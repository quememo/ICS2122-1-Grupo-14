import pandas as pd
import numpy as np


# este modulo crea un gran diccionario con el siguiente formato:
# {nodo_origen: {nodo_destino:{"distancia": xxx, "velocidades": Lista con las velocidades}}}
# ******* ojo en que formato estan los archivos de NODOS Y ARCOS **************

def diccionario_nodos(nombre_archivo_nodos, nombre_archivo_arcos):
    df_nodos = pd.read_csv(nombre_archivo_nodos, sep=";")
    df_arcos = pd.read_csv(nombre_archivo_arcos, sep=";")

    numpy_nodos = df_nodos.to_numpy()
    numpy_arcos = df_arcos.to_numpy()

    nodes_coords = {}
    for nodo in numpy_nodos:
        nodes_coords[nodo[0]] = (nodo[1], nodo[2])

    informacion_nodos = {}
    for arco in numpy_arcos:
        nodo_origen = arco[0]
        nodo_destino = arco[1]
        velocidades_arco = arco[2:]

        # calculo de la distancia
        coordenadas_nodo_origen = np.array(nodes_coords[nodo_origen])
        coordenadas_nodo_destino = np.array(nodes_coords[nodo_destino])
        distancia_entre_nodos = np.linalg.norm(coordenadas_nodo_origen - coordenadas_nodo_destino)

        # creacion del diccionario
        if nodo_origen not in informacion_nodos:
            informacion_nodos[nodo_origen] = {nodo_destino: {"distancia": distancia_entre_nodos, "velocidades": velocidades_arco}}
        else:
            informacion_nodos[nodo_origen][nodo_destino] = {"distancia": distancia_entre_nodos, "velocidades": velocidades_arco}

    return informacion_nodos, nodes_coords


if __name__ == '__main__':
    diccionario_nodos("../datos/nodos.csv", "../datos/arcos.csv")
