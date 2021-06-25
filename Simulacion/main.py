import pandas as pd
import simpy
from grafo import ClaseGrafo
import arrow
import time
from generacion_llamadas import generar_tev, generar_ubicacion
import numpy as np
import sys
from termcolor import colored
from multiprocessing import Process
from filtrar_eventos import random_sged

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1600)


def hora_actual(minutos_transcurridos):
    return fecha_inicial.shift(minutes=minutos_transcurridos)


class Ambulancia:
    class_id = 0

    def __init__(self, env, grafo, ubicacion, linea_ambulancia, cola_emergencias, estadisticas, total_ambulancias):
        self.env = env
        self.estadisticas = estadisticas
        self.grafo = grafo
        self.linea_ambulancia = linea_ambulancia
        self.total_ambulancias = total_ambulancias
        self.id = self.class_id
        self.ocupada = False
        self.en_ida = False
        self.abortar = False
        self.momento_estimado_llegada = 0
        self.time_atendido = None
        self.emergencia_en_curso = None
        self.cola_emergencias = cola_emergencias
        self.base_original = ubicacion  # ID nodo
        self.ubicacion_actual = ubicacion  # ID nodo
        self.destino_actual = None  # ID Nodo
        self.tiempo_proceso_actual = 0
        Ambulancia.class_id += 1

        self.comenzar = self.env.process(self.esperando_llamado())

    def esperando_llamado(self):
        print(f"Ambulancia {self.id}: Esperando llamado de emergencia en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")
        yield self.linea_ambulancia
        self.time_atendido = self.env.now
        self.emergencia_en_curso = self.estadisticas["llamadas_recibidas"]
        print(f"Ambulancia {self.id}: Atendiendo llamado {self.emergencia_en_curso} en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")
        ruta_emergencia = self.linea_ambulancia.value["ruta"]
        tiempo_emergencia = self.linea_ambulancia.value["tiempo"]

        self.env.process(self.moverse_a_destino(ruta_emergencia, tiempo_emergencia))

    def moverse_a_destino(self, ruta_emergencia, tiempo_emergencia):
        self.ocupada = True
        self.en_ida = True
        print(f"Ambulancia {self.id}: Se estima tardará {tiempo_emergencia} en llegar desde {self.ubicacion_actual} a {ruta_emergencia[-1]}")
        self.destino_actual = ruta_emergencia[-1]
        self.momento_estimado_llegada = self.env.now + tiempo_emergencia
        ruta_emergencia.pop(0)
        while ruta_emergencia:
            nodo_destino = ruta_emergencia[0]
            tiempo_desplazamiento = self.grafo.grafo[self.ubicacion_actual][nodo_destino]['weight']
            yield self.env.timeout(tiempo_desplazamiento)
            self.ubicacion_actual = nodo_destino
            ruta_emergencia.pop(0)

            if self.abortar:
                print(f"Ambulancia {self.id}: Me robaron el paciente {self.emergencia_en_curso}, volveré a la base original")
                self.emergencia_en_curso = None
                self.linea_ambulancia = self.env.event()
                self.abortar = False
                self.env.process(self.volver_a_base_original())
                return

        tiempo_despacho_real = self.env.now - self.time_atendido
        print(f"Ambulancia {self.id}: Se tardó {tiempo_despacho_real} en despachar, estimado de esta: {tiempo_emergencia}")
        self.estadisticas["tiempo_acumulado_despacho"].append(tiempo_despacho_real)
        print()
        self.tiempo_proceso_actual += tiempo_despacho_real
        print(f'Ambulancia {self.id}: Llegué al destino en {hora_actual(self.env.now).format("DD-MM HH:mm:ss")} y atenderé al paciente')
        self.en_ida = False
        self.destino_actual = None
        self.env.process(self.atender_paciente())

    def atender_paciente(self):
        tev_sged = random_sged()
        yield self.env.timeout(tev_sged)  #
        print(f"\nAmbulancia {self.id}: Terminé de atender al paciente en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}, ahora hay que derivarlo")
        self.estadisticas["tiempo_acumulado_atencion"].append(tev_sged)
        self.tiempo_proceso_actual += tev_sged
        self.env.process(self.derivar_paciente())

    def derivar_paciente(self):
        centro_ganador, ruta_ganadora, tiempo_derivacion = self.grafo.calcular_centro_mas_cercano(self.ubicacion_actual)
        print(f"Ambulancia {self.id}: Tengo que ir al centro cercano al nodo: {centro_ganador}")
        print(f"Ambulancia {self.id}: Estimo me tardaré {tiempo_derivacion} minutos en derivar")

        tiempo_acumulado_derivacion = 0
        ruta_ganadora.pop(0)
        while ruta_ganadora:
            nodo_destino = ruta_ganadora[0]
            tiempo_desplazamiento = self.grafo.grafo[self.ubicacion_actual][nodo_destino]['weight']
            yield self.env.timeout(tiempo_desplazamiento)
            tiempo_acumulado_derivacion += tiempo_desplazamiento
            self.ubicacion_actual = nodo_destino
            ruta_ganadora.pop(0)

        print(f"\nAmbulancia {self.id}: Ya derivé al paciente en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")
        self.estadisticas["tiempo_acumulado_derivacion"].append(tiempo_acumulado_derivacion)
        self.tiempo_proceso_actual += tiempo_acumulado_derivacion
        self.estadisticas["tiempo_acumulado_proceso"].append(self.tiempo_proceso_actual)
        self.tiempo_proceso_actual = 0
        self.time_atendido = None

        self.linea_ambulancia = self.env.event()

        print(f"Ambulancia {self.id}: Trataré de robar paciente")

        if self.robar_emergencia():
            return

        if len(self.cola_emergencias) > 0:
            print(colored(f"Ambulancia {self.id}: No regresaré a la base, hay llamadas en cola", 'yellow'))
            self.atender_cola_emergencia()
        else:
            print(f"Ambulancia {self.id}: Estoy libre, vuelvo a la base original")

            self.env.process(self.volver_a_base_original())

    def volver_a_base_original(self):
        ruta, tiempo_regreso = self.grafo.calcular_dijkstra(self.ubicacion_actual, self.base_original)
        print(f"Ambulancia {self.id}: Estimo me tardaré {tiempo_regreso} minutos en volver a la base")

        tiempo_acumulado_retorno = 0
        ruta.pop(0)
        while ruta:
            nodo_destino = ruta[0]
            tiempo_desplazamiento = self.grafo.grafo[self.ubicacion_actual][nodo_destino]['weight']
            yield self.env.timeout(tiempo_desplazamiento)
            tiempo_acumulado_retorno += tiempo_desplazamiento
            self.ubicacion_actual = nodo_destino
            ruta.pop(0)

            if len(self.cola_emergencias) > 0:
                print(colored(f"Ambulancia {self.id}: Abortando regreso, hay llamadas en cola", 'yellow'))
                self.atender_cola_emergencia()
                return

        print(f"\nAmbulancia {self.id}: Llegué a la base original en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}")
        self.ocupada = False
        self.env.process(self.esperando_llamado())

    def atender_cola_emergencia(self):
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

        self.cola_emergencias.remove(emergencia_seleccionada)
        tiempo_atraso = self.env.now - emergencia_seleccionada["hora_emergencia"]
        print(f"Ambulancia {self.id}: Atendiendo llamado en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}"
              f" con un atraso de {tiempo_atraso} minutos")
        self.time_atendido = self.env.now
        self.estadisticas["tiempo_acumulado_espera"].append(tiempo_atraso)
        self.tiempo_proceso_actual += tiempo_atraso

        self.env.process(self.moverse_a_destino(mejor_ruta_ida, mejor_tiempo_ida))

    def robar_emergencia(self):
        ambulancia_target = None
        ganancia_target = 0
        tiempo_final = None
        ruta_final = None
        tiempo_restante_final = 0

        for ambulancia in self.total_ambulancias:
            if ambulancia.en_ida and ambulancia.id != self.id:
                new_ruta_ida, new_tiempo_ida = self.grafo.calcular_dijkstra(self.ubicacion_actual, ambulancia.destino_actual)
                tiempo_restante = ambulancia.momento_estimado_llegada - self.env.now
                diferencia_new_ruta = tiempo_restante - new_tiempo_ida
                if diferencia_new_ruta > ganancia_target and diferencia_new_ruta >= 10:
                    tiempo_final = new_tiempo_ida
                    ganancia_target = diferencia_new_ruta
                    ambulancia_target = ambulancia
                    ruta_final = new_ruta_ida
                    tiempo_restante_final = tiempo_restante

        if ambulancia_target:
            print(f'Ambulancia {self.id}: Logré robarle a Ambulancia {ambulancia_target.id} la emergencia {ambulancia_target.emergencia_en_curso}')
            print(f"Ambulancia {self.id}: Esta ambulancia le faltaba {tiempo_restante_final} para llegar")
            print(f"Ambulancia {self.id}: Tengo una ganancia de {ganancia_target}")
            self.emergencia_en_curso = ambulancia_target.emergencia_en_curso
            ambulancia_target.abortar = True
            ambulancia_target.en_ida = False
            ambulancia_target.destino_actual = None
            self.time_atendido = ambulancia_target.time_atendido

            self.env.process(self.moverse_a_destino(ruta_final, tiempo_final))
            return True

        else:
            print(f"Ambulancia {self.id}: No robé nada")
            return False


class Simulacion:
    def __init__(self, dias):
        self.env = simpy.Environment()
        self.grafo = ClaseGrafo()
        self.total_ambulancias = []
        self.grafo.informacion_nodos.keys()
        self.cola_emergencias = []
        self.estadisticas = {
            "tiempo_acumulado_despacho": [],
            "tiempo_acumulado_atencion": [],
            "tiempo_acumulado_derivacion": [],
            "tiempo_acumulado_espera": [],
            "tiempo_acumulado_proceso": [],  # espera inicial + despacho + atencion + derivacion por cada emergencia
            "llamadas_recibidas": 0,
        }
        self.dias_terminados = 0

        self.stat_diario = {
            "mean": pd.DataFrame(columns=["TIEMPO_DESPACHO", "TIEMPO_ATENCION", "TIEMPO_DERIVACION", "TIEMPO_ATRASO", "TIEMPO_PROCESO"]),
            "25%": pd.DataFrame(columns=["TIEMPO_DESPACHO", "TIEMPO_ATENCION", "TIEMPO_DERIVACION", "TIEMPO_ATRASO", "TIEMPO_PROCESO"]),
            "50%": pd.DataFrame(columns=["TIEMPO_DESPACHO", "TIEMPO_ATENCION", "TIEMPO_DERIVACION", "TIEMPO_ATRASO", "TIEMPO_PROCESO"]),
            "75%": pd.DataFrame(columns=["TIEMPO_DESPACHO", "TIEMPO_ATENCION", "TIEMPO_DERIVACION", "TIEMPO_ATRASO", "TIEMPO_PROCESO"]),
            "90%": pd.DataFrame(columns=["TIEMPO_DESPACHO", "TIEMPO_ATENCION", "TIEMPO_DERIVACION", "TIEMPO_ATRASO", "TIEMPO_PROCESO"]),
        }

        self.nodos_iniciales = [0, 3, 5, 6, 16, 18, 2151, 20, 21, 2163, 3299, 38, 41, 46, 48, 58, 63, 908, 68, 3305]

        for i in range(20):
            self.total_ambulancias.append(Ambulancia(
                self.env, self.grafo, self.nodos_iniciales[i], self.env.event(), self.cola_emergencias, self.estadisticas, self.total_ambulancias))

        self.env.process(self.llamadas())
        self.env.process(self.actualizar_velocidades())
        self.env.process(self.obtener_estadisticas_diarias())
        self.env.run(until=self.cantidad_dias(dias))
        print(colored(f"\nSimulación terminada en: {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}", "green"))
        self.presentar_estadisticas()

    @staticmethod
    def cantidad_dias(dias):
        return dias * 24 * 60

    def llamadas(self):
        while True:
            tiempo_emergencia = generar_tev(hora_actual(self.env.now))
            coords_emergencia = generar_ubicacion("datos/eventos.csv", hora_actual(self.env.now))
            yield self.env.timeout(tiempo_emergencia)
            print()
            print(f"Llegó llamado en {hora_actual(self.env.now).format('DD-MM HH:mm:ss')}, tengo que mandar ambulancia")
            print(f"Hay {sum(1 for ambulance in self.total_ambulancias if not ambulance.ocupada)} ambulancias libres")

            self.estadisticas["llamadas_recibidas"] += 1

            nodo_emergencia = self.grafo.calcular_nodo_cercano(coords_emergencia)

            ambulancia_elegida = None
            tiempo_despacho_elegido = np.Infinity
            ruta_despacho_elegido = None

            for ambulancia in self.total_ambulancias:
                if not ambulancia.ocupada:
                    ruta_despacho_ambulancia, tiempo_despacho_ambulancia = self.grafo.calcular_dijkstra(ambulancia.ubicacion_actual, nodo_emergencia)
                    if tiempo_despacho_ambulancia < tiempo_despacho_elegido:
                        tiempo_despacho_elegido = tiempo_despacho_ambulancia
                        ruta_despacho_elegido = ruta_despacho_ambulancia
                        ambulancia_elegida = ambulancia

            if ambulancia_elegida is None:
                print(colored('Todas las ambulancias están ocupadas', 'red'))
                informacion_llamada_emergencia = {"coordenadas": coords_emergencia, "hora_emergencia": self.env.now}
                self.cola_emergencias.append(informacion_llamada_emergencia)

            else:
                print(f"Ambulancia elegida es: {ambulancia_elegida.id}")
                ambulancia_elegida.linea_ambulancia.succeed(value={"ruta": ruta_despacho_elegido, "tiempo": tiempo_despacho_elegido})

    def actualizar_velocidades(self):
        while True:
            yield self.env.timeout(60)
            self.grafo.actualizar_arcos(hora_actual(self.env.now).hour)

    def obtener_estadisticas_diarias(self):
        while True:
            yield self.env.timeout(60 * 24)
            self.dias_terminados += 1

            resumen = [
                pd.DataFrame(self.estadisticas["tiempo_acumulado_despacho"], columns=["TIEMPO_DESPACHO"]).describe(
                    percentiles=[.25, .5, .75, .9]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_atencion"], columns=['TIEMPO_ATENCION']).describe(
                    percentiles=[.25, .5, .75, .9]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_derivacion"], columns=['TIEMPO_DERIVACION']).describe(
                    percentiles=[.25, .5, .75, .9]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_espera"], columns=['TIEMPO_ATRASO']).describe(
                    percentiles=[.25, .5, .75, .9]),
                pd.DataFrame(self.estadisticas["tiempo_acumulado_proceso"], columns=['TIEMPO_PROCESO']).describe(
                    percentiles=[.25, .5, .75, .9]),
            ]

            tabla_resumen = pd.concat(resumen, axis=1).fillna(0)

            for index, row in tabla_resumen.iterrows():
                if index in self.stat_diario.keys():
                    self.stat_diario[index].loc[self.dias_terminados] = row

            # print(colored(f"\nFin del día {self.dias_terminados}", 'blue'))
            # print(tabla_resumen)
            # print(colored(f"Se recibieron {self.estadisticas['llamadas_recibidas']} llamadas", "blue"))
            # print(colored(f"Se completaron {len(self.estadisticas['tiempo_acumulado_proceso'])} emergencias", "blue"))

    def presentar_estadisticas(self):
        self.dias_terminados += 1
        resumen = [
            pd.DataFrame(self.estadisticas["tiempo_acumulado_despacho"], columns=["TIEMPO_DESPACHO"]).describe(
                percentiles=[.25, .5, .75, .9]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_atencion"], columns=['TIEMPO_ATENCION']).describe(
                percentiles=[.25, .5, .75, .9]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_derivacion"], columns=['TIEMPO_DERIVACION']).describe(
                percentiles=[.25, .5, .75, .9]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_espera"], columns=['TIEMPO_ATRASO']).describe(
                percentiles=[.25, .5, .75, .9]),
            pd.DataFrame(self.estadisticas["tiempo_acumulado_proceso"], columns=['TIEMPO_PROCESO']).describe(
                percentiles=[.25, .5, .75, .9]),
        ]

        tabla_resumen = pd.concat(resumen, axis=1).fillna(0)

        print(tabla_resumen)
        print()

        for index, row in tabla_resumen.iterrows():
            if index in self.stat_diario.keys():
                self.stat_diario[index].loc[self.dias_terminados] = row

        for key, value in self.stat_diario.items():
            value.to_csv(path_or_buf=f"entrega3/test/{key}_diario.csv", index=True, index_label="DIA", sep=";")


        print(colored(f"Se recibieron {self.estadisticas['llamadas_recibidas']} llamadas", "blue"))
        print(colored(f"Se completaron {len(self.estadisticas['tiempo_acumulado_proceso'])} emergencias", "blue"))
        print(colored(f"Quedaron {len(self.cola_emergencias)} pacientes sin atender", "red"))


def iniciar_simulacion():
    global fecha_inicial
    fecha_inicial = arrow.get('2021-01-01T00:00:00')
    Simulacion(1)


if __name__ == '__main__':
    start_time = time.time()
    fecha_inicial = arrow.get('2021-01-01T00:00:00')

    Simulacion(10)

    # lista_simulaciones = []
    # for i in range(7):
    #     este_proceso = Process(target=iniciar_simulacion)
    #     lista_simulaciones.append(este_proceso)
    #     este_proceso.start()
    #
    # for proceso in lista_simulaciones:
    #     proceso.join()

    print(colored(f"\n IRL Exec: {(time.time() - start_time) / 60} minutos", 'blue'))
