import pandas as pd
import numpy as np


# este modulo crea un gran diccionario con el siguiente formato:
# {nodo_origen: {nodo_destino:{"distancia": xxx, "velocidades": Lista con las velocidades}}}
# ******* ojo en que formato estan los archivos de NODOS Y ARCOS **************

def diccionario_principal(nombre_archivo_nodos, nombre_archivo_arcos):

    df_nodos = pd.read_csv(nombre_archivo_nodos, sep=";")
    df_arcos = pd.read_excel(nombre_archivo_arcos)

    numpy_nodos = df_nodos.to_numpy()
    numpy_arcos = df_arcos.to_numpy()


    nodos_distancia = {}
    for arco in numpy_arcos:
        nodo_origen = arco[0]
        nodo_destino = arco[1]
        velocidades_arco = arco[2:]


        coordenadas_encontradas = 0
        for nodo in numpy_nodos:

            if nodo[0] == nodo_origen:
                coordenada_x_nodo_origen = nodo[1]
                coordenada_y_nodo_origen = nodo[2]
                coordenadas_encontradas += 1

            if nodo[0] == nodo_destino:
                coordenada_x_nodo_destino = nodo[1]
                coordenada_y_nodo_destino = nodo[2]
                coordenadas_encontradas += 1

            if coordenadas_encontradas == 2:
                break

        # calculo de la distancia
        coordenadas_nodo_origen = np.array((coordenada_x_nodo_origen, coordenada_y_nodo_origen))
        coordenadas_nodo_destino = np.array((coordenada_x_nodo_destino, coordenada_y_nodo_destino))
        distancia_entre_nodos = np.linalg.norm(coordenadas_nodo_origen-coordenadas_nodo_destino)

        # creacion del diccionario
        if nodo_origen not in nodos_distancia:
            nodos_distancia[nodo_origen] = {nodo_destino: {"distancia": distancia_entre_nodos, "velocidades": velocidades_arco}}

        else:
            diccionario_nodos_destinos = nodos_distancia[nodo_origen]
            diccionario_nodos_destinos[nodo_destino] = {"distancia": distancia_entre_nodos, "velocidades": velocidades_arco}

    return diccionario_nodos_destinos