import networkx as nx
from info_nodos import diccionario_nodos
from obtener_bases_centros import obtener_bases, obtener_centros
import matplotlib.pyplot as plt
import numpy as np
import time
import sys


class ClaseGrafo(object):
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.poblar_grafo()

        # self.debugear()

    def poblar_grafo(self):
        self.informacion_nodos, self.coordenadas_nodos = diccionario_nodos(
            "datos/nodos.csv",
            "datos/arcos.csv")
        for nodo_origen in self.informacion_nodos:
            for nodo_destino in self.informacion_nodos[nodo_origen].keys():
                esta_distancia = self.informacion_nodos[nodo_origen][nodo_destino]["distancia"]
                esta_velocidad = self.informacion_nodos[nodo_origen][nodo_destino]["velocidades"][0]
                estos_minutos = 60 * esta_distancia / esta_velocidad

                self.grafo.add_edge(nodo_origen, nodo_destino, weight=estos_minutos)

        self.bases = obtener_bases()
        # for base in self.bases:
        #     self.grafo.add_node(base)

        self.centros = obtener_centros()
        # for centro in self.centros:
        #     self.grafo.add_node(centro)

    def plotear_grafo(self):
        # Descomentar cuando quiera graficar el plot
        self.coordenadas_nodos.update(self.bases)
        self.coordenadas_nodos.update(self.centros)
        print("Comienzo a plotear")
        plt.plot()
        nx.draw_networkx(self.grafo,
                         pos=self.coordenadas_nodos,
                         width=0.5,
                         arrowstyle="-",
                         arrowsize=5,
                         node_size=10,
                         font_size=8,
                         with_labels=True,
                         node_color="#3da98d",
                         )
        plt.show()
        # plt.savefig("fotofinal.png")

    def calcular_dijkstra(self, origen, destino):
        # Origen y Destino son ID's de nodo, NO COORDENADAS
        route = nx.dijkstra_path(
            self.grafo, source=origen, target=destino, weight='weight')
        minutos_totales = nx.dijkstra_path_length(self.grafo, source=origen, target=destino, weight='weight')
        return route, minutos_totales

    # Quiz??s luego implementar un diccionario para guardar bases y centros
    def calcular_nodo_cercano(self, tupla_coordenadas):
        distancia_minima = np.Infinity
        nodo_minimo = None
        # Si algo explota, cambiar esto a 0
        for nodo in self.coordenadas_nodos:
            distancia_euclidiana = np.linalg.norm(np.array(self.coordenadas_nodos[nodo]) - np.array(tupla_coordenadas))
            if distancia_euclidiana < distancia_minima:
                nodo_minimo = nodo
                distancia_minima = distancia_euclidiana
        return nodo_minimo

    def calcular_centro_mas_cercano(self, ubicacion_actual):
        tiempo_total = time.time()
        minuto_minimo = np.Infinity
        centro_ganador = None
        ruta_ganadora = None
        dict_nodocentro_distanciaeuclidiana = {}

        for coordenada_centro in self.centros.values():
            distancia_euclidiana = np.linalg.norm(np.array(self.coordenadas_nodos[ubicacion_actual]) - np.array(coordenada_centro))
            dict_nodocentro_distanciaeuclidiana[coordenada_centro] = distancia_euclidiana
        dict_nodocentro_distanciaeuclidiana = {k: v for k, v in sorted(dict_nodocentro_distanciaeuclidiana.items(), key=lambda item: item[1])}

        iterador = 0
        coordenadas_centros_cercanos = []
        for key, value in dict_nodocentro_distanciaeuclidiana.items():
            if iterador == 10:
                break
            coordenadas_centros_cercanos.append(key)
            iterador += 1

        for coordenada in coordenadas_centros_cercanos:
            nodo_cercano_al_centro = self.calcular_nodo_cercano(coordenada)
            ruta, minutos_demorados = self.calcular_dijkstra(ubicacion_actual, nodo_cercano_al_centro)
            if minutos_demorados < minuto_minimo:
                minuto_minimo = minutos_demorados
                centro_ganador = nodo_cercano_al_centro
                ruta_ganadora = ruta
        return centro_ganador, ruta_ganadora, minuto_minimo

    def actualizar_arcos(self, hora_actual):
        for nodo_origen, nodos_vecinos in self.informacion_nodos.items():
            for nodo_destino, info in nodos_vecinos.items():
                tiempo_desplazamiento = 60 * info["distancia"] / info["velocidades"][hora_actual]
                if tiempo_desplazamiento != self.grafo[nodo_origen][nodo_destino]["weight"]:
                    self.grafo[nodo_origen][nodo_destino]["weight"] = tiempo_desplazamiento
                else:
                    if tiempo_desplazamiento == 0:
                        continue
                    else:
                        return

    def debugear(self):
        # self.calcular_dijkstra(0, 6)
        # self.plotear_grafo()
        # nodo_buscado = self.calcular_nodo_cercano((124.8, -1.4))
        # print(f"El nodo m??s cercano es: {nodo_buscado}")
        # self.calcular_centro_mas_cercano(4065)
        # self.actualizar_arcos(0)
        # for i in range(24):
        #     self.actualizar_arcos(i)
        bases_radio20 = [
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

        lista_nodos = [self.calcular_nodo_cercano(base) for base in bases_radio20]
        print(lista_nodos)

        pass


if __name__ == '__main__':
    ClaseGrafo()
