import sys
import time
from functools import cache, lru_cache
from multiprocessing import Process
import simpy
import pandas as pd
import numpy as np
import arrow
from termcolor import colored
from grafo import ClaseGrafo
from generacion_llamadas import generar_tev, generar_ubicacion
from filtrar_eventos import random_sged, random_despacho, random_derivacion, encontrar_bases_cercanas

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1600)


def hora_actual(minutos_transcurridos):
    return fecha_inicial.shift(minutes=minutos_transcurridos)


class Ambulancia:
    class_id = 0

    def __init__(self, env, grafo, ubicacion, linea_ambulancia, cola_emergencias, estadisticas, total_ambulancias):
        self.id = self.class_id
        self.env = env
        self.estadisticas = estadisticas
        self.grafo = grafo
        self.linea_ambulancia = linea_ambulancia  # Simpy Event
        self.total_ambulancias = total_ambulancias
        self.cola_emergencias = cola_emergencias

        self.base_original = ubicacion  # ID nodo
        self.ubicacion_actual = ubicacion  # ID nodo
        self.nodo_sgte = None  # ID Nodo siguiente de trayectoria actual (puede ser ida, traslado, regreso)
        self.destino_actual = None  # ID Nodo (Destino final de trayectoria actual)

        self.ocupada = False  # Estado que es FALSE solo si está en la base original esperando, TRUE si está en terreno o acaba de comenzar
        self.en_ida = False  # Si está en ida de buscar a un paciente
        self.abortar = False  # Si le robaron el paciente que tenía asignado en la ida

        self.momento_estimado_llegada = 0  # Env.now del momento estimado en que llego
        self.tiempo_proceso_actual = 0  # Int de tiempo acumulado invertido en el proceso completo
        self.time_atendido = None  # Env.now del momento en que asigno una llamada de emergencia
        self.emergencia_en_curso = None  # ID emergencia

        self.regresando_a_base = False  # Estado de recibir llamadas TRUE SOLO SI ESTA VOLVIENDO A BASE, FALSE en caso contrario
        self.me_asignaron_llamada = False  # Estado para abortar regreso, si es que debo atender llamada
        self.ruta_actual = None  # [ ID Nodo... ]
        self.tiempo_ruta_actual = None  # Tiempo estimado me tardaré en llegar al destino final

        Ambulancia.class_id += 1

        self.env.process(self.esperando_llamado())

    def esperando_llamado(self):
        self.linea_ambulancia = self.env.event()
        #         # print(f"Ambulancia {self.id}: Esperando llamado de emergencia en base {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")
        yield self.linea_ambulancia
        self.time_atendido = self.env.now
        self.emergencia_en_curso = self.linea_ambulancia.value["id"]
        # print(f"Ambulancia {self.id}: Atendiendo llamado {self.emergencia_en_curso} en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')},"
        #       f" me preparo para salir")
        self.ocupada = True
        ruta_emergencia = self.linea_ambulancia.value["ruta"]
        tiempo_emergencia = self.linea_ambulancia.value["tiempo"]

        # Retraso despacho
        retraso_despacho = random_despacho()
        yield self.env.timeout(retraso_despacho)
        self.estadisticas["tiempo_acumulado_despacho"].append(retraso_despacho)
        self.tiempo_proceso_actual += retraso_despacho
        # print(f"Ambulancia {self.id}: Ya salí en busca del paciente luego de {retraso_despacho} minutos")

        self.env.process(self.moverse_a_destino(ruta_emergencia, tiempo_emergencia))
        return

    def moverse_a_destino(self, ruta_emergencia, tiempo_emergencia):
        self.regresando_a_base = False
        self.ocupada = True
        self.en_ida = True
        self.destino_actual = ruta_emergencia[-1]
        # print(f"Ambulancia {self.id}: Se estima tardará {tiempo_emergencia} en llegar desde {self.ubicacion_actual} a {ruta_emergencia[-1]}")
        self.momento_estimado_llegada = self.env.now + tiempo_emergencia
        ruta_emergencia.pop(0)
        while ruta_emergencia:
            self.nodo_sgte = ruta_emergencia[0]
            velocidad_inicial = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            tiempo_desplazamiento = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            yield self.env.timeout(tiempo_desplazamiento)
            velocidad_final = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            self.ubicacion_actual = self.nodo_sgte
            ruta_emergencia.pop(0)

            if self.abortar:
                # print(f"Ambulancia {self.id}: Me robaron el paciente {self.emergencia_en_curso}, evaluaré decisión")
                self.emergencia_en_curso = None
                self.abortar = False

                if self.decision_ambulancia_libre():
                    return
                else:
                    # print(f"Ambulancia {self.id}: Estoy libre, vuelvo a la base original")
                    self.env.process(self.recibir_llamado_en_transcurso_hacia_base())
                    self.env.process(self.volver_a_base_original())
                    return

            if velocidad_final != velocidad_inicial:
                # print(f"Ambulancia {self.id}: Cambió la velocidad a mitad de arco IDA, recalculo ruta")
                new_ruta, new_tiempo_estimado = self.grafo.calcular_dijkstra(self.ubicacion_actual, self.destino_actual)
                new_ruta.pop(0)
                ruta_emergencia = new_ruta
                continue

        tiempo_ida_real = self.env.now - self.time_atendido
        # print(f"Ambulancia {self.id}: Se tardó {tiempo_ida_real} en llegar hasta el paciente, estimado de esta: {tiempo_emergencia}")
        self.estadisticas["tiempo_acumulado_ida"].append(tiempo_ida_real)
        self.tiempo_proceso_actual += tiempo_ida_real
        # print(f'Ambulancia {self.id}: Llegué al destino en {hora_actual(self.env.now).format("DD-MM HH:mm:ss")} y atenderé al paciente')
        self.en_ida = False
        self.destino_actual = None
        self.env.process(self.atender_paciente())

    def atender_paciente(self):
        tev_sged = random_sged()
        yield self.env.timeout(tev_sged)  #
        # print(f"\nAmbulancia {self.id}: Terminé de atender al paciente en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}, ahora hay que trasladarlo")
        self.estadisticas["tiempo_acumulado_atencion"].append(tev_sged)
        self.tiempo_proceso_actual += tev_sged
        self.env.process(self.trasladar_paciente())

    def trasladar_paciente(self):
        centro_ganador, ruta_ganadora, tiempo_traslado = self.grafo.calcular_centro_mas_cercano(self.ubicacion_actual)
        # print(f"Ambulancia {self.id}: Tengo que ir al centro cercano al nodo: {centro_ganador}")
        # print(f"Ambulancia {self.id}: Estimo me tardaré {tiempo_traslado} minutos en trasladar paciente")

        tiempo_acumulado_traslado = 0
        ruta_ganadora.pop(0)
        while ruta_ganadora:
            self.nodo_sgte = ruta_ganadora[0]
            velocidad_inicial = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            tiempo_desplazamiento = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            yield self.env.timeout(tiempo_desplazamiento)
            velocidad_final = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            tiempo_acumulado_traslado += tiempo_desplazamiento
            self.ubicacion_actual = self.nodo_sgte
            ruta_ganadora.pop(0)

            if velocidad_final != velocidad_inicial:
                # print(f"Ambulancia {self.id}: Cambió la velocidad a mitad de arco en TRASLADO, recalculo ruta")
                new_ruta, new_tiempo_estimado = self.grafo.calcular_dijkstra(self.ubicacion_actual, centro_ganador)
                new_ruta.pop(0)
                ruta_ganadora = new_ruta
                continue

        # print(f"\nAmbulancia {self.id}: Ya trasladé al paciente en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}, toca derivarlo ahora")
        self.estadisticas["tiempo_acumulado_traslado"].append(tiempo_acumulado_traslado)
        self.tiempo_proceso_actual += tiempo_acumulado_traslado

        # Retraso derivacion
        retraso_derivacion = random_derivacion()
        yield self.env.timeout(retraso_derivacion)
        self.estadisticas["tiempo_acumulado_derivacion"].append(retraso_derivacion)
        self.tiempo_proceso_actual += retraso_derivacion
        # print(f"Ambulancia {self.id}: Terminé de derivarlo, luego de {retraso_derivacion} minutos")

        self.estadisticas["tiempo_acumulado_proceso"].append(self.tiempo_proceso_actual)
        self.tiempo_proceso_actual = 0
        self.time_atendido = None

        # print(f"Ambulancia {self.id}: Evaluaré que decisión tomo justo luego de terminar traslado paciente")
        if self.decision_ambulancia_libre():
            return
        else:
            # print(f"Ambulancia {self.id}: Estoy libre, vuelvo a la base original")
            self.env.process(self.recibir_llamado_en_transcurso_hacia_base())
            self.env.process(self.volver_a_base_original())
            return

    def decision_ambulancia_libre(self):
        # Prioridad 1: Atiendo que lleva más tiempo esperando
        if self.atender_emergencia_prioritaria():
            return True

        # emergencia_cercana, ruta_cercana, tiempo_cercano = self.encontrar_cola_emergencia_cercana()

        # Prioridad 2: Atiendo la cola más cercana
        # if emergencia_cercana and tiempo_cercano <= 10:
        #     self.cola_emergencias.remove(emergencia_cercana)
        #     tiempo_atraso = self.env.now - emergencia_cercana["hora_emergencia"]
        #         #     print(f"Ambulancia {self.id}: Atendiendo llamado cercano (< 15 min) PRIORIDAD 2 en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}"
        #           f" con un atraso de {tiempo_atraso} minutos")
        #     self.emergencia_en_curso = self.estadisticas["llamadas_recibidas"]
        #     self.time_atendido = self.env.now
        #     self.estadisticas["tiempo_acumulado_atraso"].append(tiempo_atraso)
        #     self.tiempo_proceso_actual += tiempo_atraso
        #
        #     self.env.process(self.moverse_a_destino(ruta_cercana, tiempo_cercano))
        #     return True

        ambulancia_robable, ruta_robo, tiempo_robo, ganancia_robo = self.encontrar_emergencia_robable()

        if ambulancia_robable:
            # print(f"Ambulancia {self.id}: Le robo a Ambulancia {ambulancia_robable.id} la emergencia {ambulancia_robable.emergencia_en_curso}")
            self.emergencia_en_curso = ambulancia_robable.emergencia_en_curso
            ambulancia_robable.abortar = True
            ambulancia_robable.en_ida = False
            ambulancia_robable.destino_actual = None
            self.time_atendido = ambulancia_robable.time_atendido

            self.env.process(self.moverse_a_destino(ruta_robo, tiempo_robo))
            return True

        # elif ambulancia_robable and not emergencia_cercana:
        #         #     print(f"Ambulancia {self.id}: Efectivamente realizo el robo, ya que no hay cola")
        #     self.emergencia_en_curso = ambulancia_robable.emergencia_en_curso
        #     ambulancia_robable.abortar = True
        #     ambulancia_robable.en_ida = False
        #     ambulancia_robable.destino_actual = None
        #     self.time_atendido = ambulancia_robable.time_atendido
        #
        #     self.env.process(self.moverse_a_destino(ruta_robo, tiempo_robo))
        #     return True

        # elif not ambulancia_robable and emergencia_cercana:
        #     # SOLO EMERGENCIA EN COLA
        #         #     # print(f"Ambulancia {self.id}: Solo puedo atender la cola")
        #     self.cola_emergencias.remove(emergencia_cercana)
        #     tiempo_atraso = self.env.now - emergencia_cercana["hora_emergencia"]
        #         #     print(f"Ambulancia {self.id}: Atendiendo llamado cercano (no hubo robo) en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}"
        #           f" con un atraso de {tiempo_atraso} minutos")
        #     self.emergencia_en_curso = self.estadisticas["llamadas_recibidas"]
        #     self.time_atendido = self.env.now
        #     self.estadisticas["tiempo_acumulado_atraso"].append(tiempo_atraso)
        #     self.tiempo_proceso_actual += tiempo_atraso
        #
        #     self.env.process(self.moverse_a_destino(ruta_cercana, tiempo_cercano))
        #     return True

        else:
            return False

    def volver_a_base_original(self):
        self.regresando_a_base = True
        ruta, tiempo_regreso = self.grafo.calcular_dijkstra(self.ubicacion_actual, self.base_original)
        # print(f"Ambulancia {self.id}: Estimo me tardaré {tiempo_regreso} minutos en volver a la base")

        tiempo_acumulado_retorno = 0
        ruta.pop(0)

        while ruta:
            self.nodo_sgte = ruta[0]
            velocidad_inicial = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            tiempo_desplazamiento = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            yield self.env.timeout(tiempo_desplazamiento)
            velocidad_final = self.grafo.grafo[self.ubicacion_actual][self.nodo_sgte]['weight']
            tiempo_acumulado_retorno += tiempo_desplazamiento
            self.ubicacion_actual = self.nodo_sgte
            ruta.pop(0)

            if self.me_asignaron_llamada:
                # print(f"Ambulancia {self.id}: Me asignaron la llamada desde arriba, voy a buscar paciente")
                self.me_asignaron_llamada = False
                self.env.process(self.moverse_a_destino(self.ruta_actual, self.tiempo_ruta_actual))
                return

            # Ahora reviso si puedo hacer algo
            # print(f"Ambulancia {self.id}: Evaluaré que decisión tomo mientras regreso a la base")
            if self.decision_ambulancia_libre():
                return
            else:
                # print(f"Ambulancia {self.id}: No cambié mi decisión, sigo volviendo a la base")
                if velocidad_final != velocidad_inicial:
                    # print(f"Ambulancia {self.id}: Cambió la velocidad a mitad de arco en REGRESO, recalculo ruta")
                    new_ruta, new_tiempo_estimado = self.grafo.calcular_dijkstra(self.ubicacion_actual, self.base_original)
                    new_ruta.pop(0)
                    ruta = new_ruta
                    continue

        # print(f"\nAmbulancia {self.id}: Llegué a la base original en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")
        self.ocupada = False
        self.regresando_a_base = False
        self.env.process(self.esperando_llamado())

    def encontrar_cola_emergencia_cercana(self):
        mejor_tiempo_ida = np.Infinity
        mejor_ruta_ida = None
        emergencia_seleccionada = None

        for emergencia in self.cola_emergencias:
            nodo_cercano = self.grafo.calcular_nodo_cercano(emergencia["coordenadas"])
            ruta_ida, tiempo_ida = self.grafo.calcular_dijkstra(self.ubicacion_actual, nodo_cercano)
            if tiempo_ida < mejor_tiempo_ida:
                mejor_tiempo_ida = tiempo_ida
                mejor_ruta_ida = ruta_ida
                emergencia_seleccionada = emergencia

        if mejor_ruta_ida:
            # print(f"Ambulancia {self.id}: Hay una emergencia en cola (criterio cercania) a {mejor_tiempo_ida} minutos")
            return emergencia_seleccionada, mejor_ruta_ida, mejor_tiempo_ida
        else:
            return None, None, None

    def atender_emergencia_prioritaria(self):
        # elige el que lleva más atraso
        tiempo_max_atraso = 0
        emergencia_elegida = None
        for emergencia in self.cola_emergencias:
            tiempo_atraso = self.env.now - emergencia['hora_emergencia']
            if tiempo_atraso > tiempo_max_atraso:
                tiempo_max_atraso = tiempo_atraso
                emergencia_elegida = emergencia

        if emergencia_elegida:
            # print(colored(f"Ambulancia {self.id}: Existe alguien en la cola que es PRIORIDAD 1, tengo que atenderlo YA", 'yellow'))
            self.cola_emergencias.remove(emergencia_elegida)
            # print(f"Ambulancia {self.id}: Atendiendo llamado prioritario en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}"
            #       f" con un atraso de {tiempo_max_atraso} minutos")
            self.emergencia_en_curso = emergencia_elegida["id"]
            self.time_atendido = self.env.now
            self.estadisticas["tiempo_acumulado_atraso"].append(tiempo_max_atraso)
            self.tiempo_proceso_actual += tiempo_max_atraso
            nodo_cercano = self.grafo.calcular_nodo_cercano(emergencia_elegida["coordenadas"])
            ruta_ida, tiempo_ida = self.grafo.calcular_dijkstra(self.ubicacion_actual, nodo_cercano)

            self.env.process(self.moverse_a_destino(ruta_ida, tiempo_ida))
            return True
        else:
            return False

    def encontrar_emergencia_robable(self):
        total_ganancias = []
        ambulancia_target = None
        ganancia_target = 0
        tiempo_final = None
        ruta_final = None
        tiempo_restante_final = 0
        for ambulancia in self.total_ambulancias:
            if ambulancia.en_ida and ambulancia.id != self.id:
                new_ruta_ida, new_tiempo_ida = self.grafo.calcular_dijkstra(self.ubicacion_actual, ambulancia.destino_actual)
                tiempo_restante = ambulancia.momento_estimado_llegada - self.env.now

                # if tiempo_restante < 0:
                #                 #   print(colored(f"ESTOY EN CASO BORDE DEL ROBO, tiempo: {tiempo_restante}", 'red'))

                diferencia_new_ruta = tiempo_restante - new_tiempo_ida
                total_ganancias.append(diferencia_new_ruta)
                if diferencia_new_ruta > ganancia_target and diferencia_new_ruta > 10:
                    tiempo_final = new_tiempo_ida
                    ganancia_target = diferencia_new_ruta
                    ambulancia_target = ambulancia
                    ruta_final = new_ruta_ida
                    tiempo_restante_final = tiempo_restante

        if ambulancia_target:
            # print(f'Ambulancia {self.id}: Podría robar a Ambulancia {ambulancia_target.id} la emergencia {ambulancia_target.emergencia_en_curso}')
            # print(f"Ambulancia {self.id}: Esta ambulancia le falta {tiempo_restante_final} para llegar")
            # print(f"Ambulancia {self.id}: Tendría una ganancia de {ganancia_target}")
            return ambulancia_target, ruta_final, tiempo_final, ganancia_target

        else:
            try:
                # print(f"Ambulancia {self.id}: No hay nada que robar, el mejor candidato era: {max(total_ganancias)}")
                return None, None, None, None
            except ValueError:
                #                 # print(f"Ambulancia {self.id}: No hay nada que robar, no habian candidatos")
                return None, None, None, None

    def recibir_llamado_en_transcurso_hacia_base(self):
        self.linea_ambulancia = self.env.event()
        yield self.linea_ambulancia
        self.me_asignaron_llamada = True
        self.regresando_a_base = False

        self.time_atendido = self.env.now
        self.emergencia_en_curso = self.linea_ambulancia.value["id"]
        # print(f"Ambulancia {self.id}: Apenas llegue al siguiente nodo, atiendo emergencia {self.emergencia_en_curso}"
        #       f" en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")

        self.ruta_actual = self.linea_ambulancia.value["ruta"]
        self.tiempo_ruta_actual = self.linea_ambulancia.value["tiempo"]

        return


class Simulacion:
    def __init__(self, bases_asignadas, dias, core):
        self.env = simpy.Environment()
        self.dias_limite = dias
        self.core = core
        self.grafo = ClaseGrafo()
        self.total_ambulancias = []
        self.cola_emergencias = []
        self.nodos_iniciales = self.convertir_bases_a_nodos(bases_asignadas)
        # self.nodos_iniciales = [0, 3, 5, 6, 16, 18, 2151, 20, 21, 2163, 3299, 38, 41, 46, 48, 58, 63, 908, 68, 3305]

        self.estadisticas = {
            "tiempo_acumulado_atraso": [],
            "tiempo_acumulado_despacho": [],
            "tiempo_acumulado_ida": [],
            "tiempo_acumulado_atencion": [],
            "tiempo_acumulado_traslado": [],
            "tiempo_acumulado_derivacion": [],
            "tiempo_acumulado_proceso": [],  # atraso inicial + despacho + ida + atencion + traslado + derivacion (por cada emergencia)
            "llamadas_recibidas": 0,
        }
        self.dias_terminados = 0
        self.stat_diario = {
            "count": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "std": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "mean": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "25%": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "50%": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "75%": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "85%": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
            "95%": pd.DataFrame(
                columns=["TIEMPO_ATRASO", "TIEMPO_DESPACHO", "TIEMPO_IDA", "TIEMPO_ATENCION", "TIEMPO_TRASLADO", "TIEMPO_DERIVACION", "TIEMPO_PROCESO"]),
        }

        for i in range(20):
            self.total_ambulancias.append(Ambulancia(
                self.env, self.grafo, self.nodos_iniciales[i], self.env.event(), self.cola_emergencias, self.estadisticas, self.total_ambulancias))

    @staticmethod
    def cantidad_dias(dias):
        return dias * 24 * 60

    def llamadas(self):
        while True:
            tiempo_emergencia = generar_tev(hora_actual(self.env.now))
            coords_emergencia = generar_ubicacion("datos/eventos.csv", hora_actual(self.env.now))
            yield self.env.timeout(tiempo_emergencia)
            self.estadisticas["llamadas_recibidas"] += 1
            # print(f"\nSISTEMA: Llegó llamado {self.estadisticas['llamadas_recibidas']} en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')},"
            #       f" tengo que mandar ambulancia")
            # print(f"SISTEMA: Hay {sum(1 for ambulance in self.total_ambulancias if not ambulance.ocupada)} ambulancias libres en base")
            # print(f"SISTEMA: Hay {sum(1 for ambulance in self.total_ambulancias if ambulance.regresando_a_base)}"
            #       f" ambulancias volviendo a la base que pueden ser asignadas")

            nodo_emergencia = self.grafo.calcular_nodo_cercano(coords_emergencia)

            ambulancia_elegida = None
            tiempo_ida_elegido = np.Infinity
            ruta_ida_elegido = None
            eleccion_final = None

            for ambulancia in self.total_ambulancias:
                if not ambulancia.ocupada or ambulancia.regresando_a_base:
                    if ambulancia.regresando_a_base:
                        ubicacion_considerar = ambulancia.nodo_sgte
                        eleccion_temporal = "regresando"
                    else:
                        ubicacion_considerar = ambulancia.ubicacion_actual
                        eleccion_temporal = "en base"

                    ruta_ida_ambulancia, tiempo_ida_ambulancia = self.grafo.calcular_dijkstra(ubicacion_considerar, nodo_emergencia)
                    if tiempo_ida_ambulancia < tiempo_ida_elegido:
                        tiempo_ida_elegido = tiempo_ida_ambulancia
                        ruta_ida_elegido = ruta_ida_ambulancia
                        ambulancia_elegida = ambulancia
                        eleccion_final = eleccion_temporal

            if ambulancia_elegida is None:
                # print(colored('SISTEMA: Todas las ambulancias están ocupadas', 'red'))
                informacion_llamada_emergencia = {"coordenadas": coords_emergencia, "hora_emergencia": self.env.now,
                                                  "id": self.estadisticas["llamadas_recibidas"]}
                self.cola_emergencias.append(informacion_llamada_emergencia)

            else:
                # print(f"SISTEMA: Ambulancia elegida es: {ambulancia_elegida.id} (Estaba {eleccion_final})")
                ambulancia_elegida.linea_ambulancia.succeed(
                    value={"ruta": ruta_ida_elegido, "tiempo": tiempo_ida_elegido, "id": self.estadisticas["llamadas_recibidas"]})

    def actualizar_velocidades(self):
        while True:
            yield self.env.timeout(60)
            self.grafo.actualizar_arcos(hora_actual(self.env.now).hour)

    def obtener_estadisticas_diarias(self):
        while True:
            yield self.env.timeout(60 * 24)
            self.dias_terminados += 1
            print(f"SYSTEM: Terminó el día {self.dias_terminados}")

            resumen = [
                pd.DataFrame(self.estadisticas["tiempo_acumulado_atraso"], columns=['TIEMPO_ATRASO']).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_despacho"], columns=["TIEMPO_DESPACHO"]).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_ida"], columns=["TIEMPO_IDA"]).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_atencion"], columns=['TIEMPO_ATENCION']).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_traslado"], columns=['TIEMPO_TRASLADO']).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_derivacion"], columns=['TIEMPO_DERIVACION']).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_proceso"], columns=['TIEMPO_PROCESO']).describe(
                    percentiles=[.25, .5, .75, .85, .95]),
            ]

            tabla_resumen = pd.concat(resumen, axis=1).fillna(0)

            for index, row in tabla_resumen.iterrows():
                if index in self.stat_diario.keys():
                    self.stat_diario[index].loc[self.dias_terminados] = row

    def presentar_estadisticas(self):
        self.dias_terminados += 1
        resumen = [
            pd.DataFrame(self.estadisticas["tiempo_acumulado_atraso"], columns=['TIEMPO_ATRASO']).describe(
                percentiles=[.25, .5, .75, .85, .95]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_despacho"], columns=["TIEMPO_DESPACHO"]).describe(
                percentiles=[.25, .5, .75, .85, .95]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_ida"], columns=["TIEMPO_IDA"]).describe(
                percentiles=[.25, .5, .75, .85, .95]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_atencion"], columns=['TIEMPO_ATENCION']).describe(
                percentiles=[.25, .5, .75, .85, .95]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_traslado"], columns=['TIEMPO_TRASLADO']).describe(
                percentiles=[.25, .5, .75, .85, .95]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_derivacion"], columns=['TIEMPO_DERIVACION']).describe(
                percentiles=[.25, .5, .75, .85, .95]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_proceso"], columns=['TIEMPO_PROCESO']).describe(
                percentiles=[.25, .5, .75, .85, .95]),
        ]

        tabla_resumen = pd.concat(resumen, axis=1).fillna(0)
        try:
            tabla_resumen = tabla_resumen.drop(['unique', 'top', 'freq'])
        except KeyError:
            pass

        print(tabla_resumen)
        print()

        for index, row in tabla_resumen.iterrows():
            if index in self.stat_diario.keys():
                self.stat_diario[index].loc[self.dias_terminados] = row

        for key, value in self.stat_diario.items():
            value.to_csv(path_or_buf=f"entrega3/cores/{self.core}/{key}_diario.csv", index=True, index_label="DIA", sep=";")

        print(colored(f"SISTEMA: Se recibieron {self.estadisticas['llamadas_recibidas']} llamadas", "blue"))
        print(colored(f"SISTEMA: Se completaron {len(self.estadisticas['tiempo_acumulado_proceso'])} emergencias", "blue"))
        print(colored(f"SISTEMA: Quedaron {len(self.cola_emergencias)} emergencias en cola sin atender", "red"))

        return tabla_resumen

    def convertir_bases_a_nodos(self, lista_bases):
        lista_nodos = [self.grafo.calcular_nodo_cercano(base) for base in lista_bases]
        return lista_nodos

    def comenzar(self):
        print(f"Comienza una simulación de {self.dias_limite} dias")
        self.env.process(self.llamadas())
        self.env.process(self.actualizar_velocidades())
        self.env.process(self.obtener_estadisticas_diarias())
        self.env.run(until=self.cantidad_dias(self.dias_limite))
        print(colored(f"\nSimulación terminada en: {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}", "green"))
        return self.presentar_estadisticas()


def iniciar_simulacion(bases_iniciales, core):
    global fecha_inicial
    fecha_inicial = arrow.get('2021-01-01T00:00:00')
    una_simulacion = Simulacion(bases_iniciales, 90, core)
    resumen = una_simulacion.comenzar()


def alterar_bases_iniciales(bases_iniciales):
    index_ambulancia = 0
    conjunto_bases_iniciales = [bases_iniciales]
    base_modificable = bases_iniciales[index_ambulancia]

    for remplazo_base in encontrar_bases_cercanas(base_modificable):
        new_lista = bases_iniciales.copy()
        new_lista[index_ambulancia] = list(remplazo_base)
        conjunto_bases_iniciales.append(new_lista)

    return conjunto_bases_iniciales


def memo_heuristica(bases_iniciales):
    conjunto_bases = alterar_bases_iniciales(bases_iniciales)
    lista_procesos_simulacion = []
    idx_core = 0
    for unas_bases_iniciales in conjunto_bases:
        proceso = Process(target=iniciar_simulacion, args=(unas_bases_iniciales, idx_core))
        idx_core += 1
        lista_procesos_simulacion.append(proceso)
        proceso.start()

    for cada_proceso in lista_procesos_simulacion:
        cada_proceso.join()


if __name__ == '__main__':
    start_time = time.time()
    fecha_inicial = arrow.get('2021-01-01T00:00:00')
    bases_radio20_mlcp = [
        [35.1, 45.4],
        [98.7, 77.8],
        [58.8, 62],
        [107.4, 111.3],
        [80.9, 68.6],
        [26.1, 0.2],
        [97.2, 46.3],
        [29.6, 91.7],
        [83.6, 40.9],
        [72.8, -7.1],
        [33.5, 39.7],
        [22.1, 82.2],
        [39.5, 61.9],
        [54.9, 99.4],
        [63.4, 82.1],
        [121.7, -23.5],
        [4.7, -30.5],
        [21.7, -20.8],
        [155.4, -9.2],
        [131.7, 57.4]
    ]

    memo_heuristica(bases_radio20_mlcp)

    print(colored(f"\n IRL Exec: {(time.time() - start_time) / 60} minutos", 'blue'))
