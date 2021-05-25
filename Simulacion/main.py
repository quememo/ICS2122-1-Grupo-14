import pandas as pd
import simpy
from grafo import ClaseGrafo
import arrow
import time
from generacion_llamadas import generar_tev, generar_ubicacion
import numpy as np
import sys
from termcolor import colored


def hora_actual(minutos_transcurridos):
    return fecha_inicial.shift(minutes=minutos_transcurridos)


class Ambulancia:
    class_id = 0

    def __init__(self, env, grafo, ubicacion, linea_ambulancia, cola_emergencias, estadisticas):
        self.env = env
        self.estadisticas = estadisticas
        self.grafo = grafo
        self.linea_ambulancia = linea_ambulancia
        self.id = self.class_id
        self.ocupada = False
        self.cola_emergencias = cola_emergencias
        self.base_original = ubicacion  # ID nodo
        self.ubicacion_actual = ubicacion  # ID nodo
        self.tiempo_proceso_actual = 0
        Ambulancia.class_id += 1

        self.comenzar = self.env.process(self.esperando_llamado())

    def esperando_llamado(self):
        print(f"Ambulancia {self.id}: Esperando llamado de emergencia en {self.env.now}")
        yield self.linea_ambulancia
        print(f"Ambulancia {self.id}: Atendiendo llamado en {self.env.now}")
        ruta_emergencia = self.linea_ambulancia.value["ruta"]
        tiempo_emergencia = self.linea_ambulancia.value["tiempo"]
        self.ocupada = True

        self.env.process(self.moverse_a_destino(ruta_emergencia, tiempo_emergencia))

    def moverse_a_destino(self, ruta_emergencia, tiempo_emergencia):
        nodo_destino = ruta_emergencia[-1]
        print(f"Ambulancia {self.id}: Mi ruta será {ruta_emergencia}")
        print(f"Ambulancia {self.id}: Se estima tardará {tiempo_emergencia} minutos en llegar")
        yield self.env.timeout(tiempo_emergencia)
        print(f'\nAmbulancia {self.id}: Llegué al destino en {self.env.now}')
        self.estadisticas["tiempo_acumulado_despacho"].append(tiempo_emergencia)
        self.tiempo_proceso_actual += tiempo_emergencia

        self.ubicacion_actual = nodo_destino
        self.env.process(self.atender_paciente())

    def atender_paciente(self):
        print(f'Ambulancia {self.id}: Voy a atender al paciente')
        tev_gaussiano = np.random.wald(mean=16.48, scale=35.64)
        yield self.env.timeout(tev_gaussiano)  #
        print(f"\nAmbulancia {self.id}: Terminé de atender al paciente en {self.env.now}, ahora hay que derivarlo")
        self.estadisticas["tiempo_acumulado_atencion"].append(tev_gaussiano)
        self.tiempo_proceso_actual += tev_gaussiano
        self.env.process(self.derivar_paciente())

    def derivar_paciente(self):
        centro_ganador, ruta_ganadora, tiempo_derivacion = self.grafo.calcular_centro_mas_cercano(self.ubicacion_actual)
        print(f"Ambulancia {self.id}: Tengo que ir al centro cercano al nodo: {centro_ganador}")
        print(f"Ambulancia {self.id}: Mi ruta será {ruta_ganadora}")
        print(f"Ambulancia {self.id}: Estimo me tardaré {tiempo_derivacion} minutos")

        yield self.env.timeout(tiempo_derivacion)
        print(f"\nAmbulancia {self.id}: Ya derivé al paciente en {self.env.now}")
        self.estadisticas["tiempo_acumulado_derivacion"].append(tiempo_derivacion)
        self.tiempo_proceso_actual += tiempo_derivacion
        self.estadisticas["tiempo_acumulado_proceso"].append(self.tiempo_proceso_actual)
        self.tiempo_proceso_actual = 0

        self.ocupada = False
        self.linea_ambulancia = self.env.event()
        self.ubicacion_actual = centro_ganador

        if len(self.cola_emergencias) > 0:
            print(colored('Hay un paciente esperando su ambulancia, buscaré al más cercano', 'yellow'))
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
            print(f"Ambulancia {self.id}: Atendiendo llamado en {self.env.now} con un atraso de {tiempo_atraso} minutos")
            self.estadisticas["tiempo_acumulado_espera"].append(tiempo_atraso)
            self.tiempo_proceso_actual += tiempo_atraso
            self.ocupada = True

            self.env.process(self.moverse_a_destino(mejor_ruta_ida, mejor_tiempo_ida))
        else:
            print(f"Ambulancia {self.id}: Ahora tengo que volver a la base original")
            self.ocupada = True
            self.env.process(self.volver_a_base_original())

    def volver_a_base_original(self):
        ruta, tiempo_regreso = self.grafo.calcular_dijkstra(self.ubicacion_actual, self.base_original)
        print(f"Ambulancia {self.id}: Mi ruta será {ruta}")
        print(f"Ambulancia {self.id}: Me tardaré {tiempo_regreso} minutos")
        yield self.env.timeout(tiempo_regreso)
        print(f"\nAmbulancia {self.id}: Llegué a la base original en {hora_actual(self.env.now)}")
        self.ubicacion_actual = self.base_original
        self.ocupada = False
        self.env.process(self.esperando_llamado())


class Simulacion:
    def __init__(self):
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

        self.nodos_iniciales = [0, 3, 5, 6, 16, 18, 2151, 20, 21, 2163, 3299, 38, 41, 46, 48, 58, 63, 908, 68, 3305]

        for i in range(20):
            self.total_ambulancias.append(Ambulancia(
                self.env, self.grafo, self.nodos_iniciales[i], self.env.event(), self.cola_emergencias, self.estadisticas))

        self.env.process(self.llamadas())
        self.env.process(self.actualizar_velocidades())
        self.env.run(until=self.cantidad_dias(7))
        print(colored(f"\nSimulación terminada en: {hora_actual(self.env.now)}", "green"))
        self.presentar_estadisticas()

    @staticmethod
    def cantidad_dias(dias):
        return dias * 24 * 60

    def llamadas(self):
        while True:
            tiempo_emergencia = generar_tev(hora_actual(self.env.now))
            coords_emergencia = generar_ubicacion("datos/eventos.csv")
            yield self.env.timeout(tiempo_emergencia)
            print()
            print(f"Llegó un llamado en {hora_actual(self.env.now)}, tengo que mandar ambulancia")
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

    def presentar_estadisticas(self):
        self.resumen = {
            "TA_despacho": pd.DataFrame(self.estadisticas["tiempo_acumulado_despacho"], columns=['Tiempo Despacho']),
            "TA_atencion": pd.DataFrame(self.estadisticas["tiempo_acumulado_atencion"], columns=['Tiempo Atencion']),
            "TA_derivacion": pd.DataFrame(self.estadisticas["tiempo_acumulado_derivacion"], columns=['Tiempo Derivacion']),

            "TA_atraso": pd.DataFrame(self.estadisticas["tiempo_acumulado_espera"], columns=['Tiempo Atraso']),
            "TA_proceso": pd.DataFrame(self.estadisticas["tiempo_acumulado_proceso"], columns=['Tiempo Proceso']),
        }

        print(self.resumen["TA_despacho"].describe())
        print(self.resumen["TA_atencion"].describe())
        print(self.resumen["TA_derivacion"].describe())
        print(self.resumen["TA_atraso"].describe())
        print(self.resumen["TA_proceso"].describe())

        print(colored(f"Se recibieron {self.estadisticas['llamadas_recibidas']} llamadas de emergencia", "blue"))
        print(colored(f"Se completaron {len(self.estadisticas['tiempo_acumulado_proceso'])} emergencias", "blue"))
        print(colored(f"Quedaron {len(self.cola_emergencias)} pacientes sin atender", "red"))


if __name__ == '__main__':
    start_time = time.time()
    fecha_inicial = arrow.get('2021-01-01T00:00:00')
    Simulacion()
    print(colored(f"\n IRL Exec: {(time.time() - start_time) / 60} minutos", 'blue'))
