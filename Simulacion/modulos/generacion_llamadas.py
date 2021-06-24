import pandas as pd
import numpy as np
import time
from random import randint, uniform
from math import cos, sin
import matplotlib.pyplot as plt
import arrow
import sys


def generar_ubicacion(nombre_archivo_eventos, arrow_actual):
    hora_actual = str(arrow_actual.hour)
    if len(hora_actual) == 1:
        hora_actual = f"0{hora_actual}"
    pandas_eventos = pd.read_csv(nombre_archivo_eventos, sep=";")
    df_filtrados = pandas_eventos.loc[(pandas_eventos['HORARIO'] >= f"{hora_actual}:00") & (pandas_eventos['HORARIO'] <= f"{hora_actual}:59")]
    # print(df_filtrados.to_string())
    numpy_eventos = df_filtrados.to_numpy()

    evento_aleatorio = numpy_eventos[randint(0, len(numpy_eventos) - 1)]
    coords_evento = (evento_aleatorio[0], evento_aleatorio[1])
    radio = 1
    radio_aleatorio = uniform(0, radio)
    angulo_aleatorio = uniform(0, 360)
    new_coords = (radio_aleatorio * cos(angulo_aleatorio), radio_aleatorio * sin(angulo_aleatorio))
    coordenadas_nuevo_evento = (coords_evento[0] + new_coords[0], coords_evento[1] + new_coords[1])

    # print(f"Vieja coordenada: {coords_evento}")
    # print(f"Nueva coordenada: {coordenadas_nuevo_evento}")
    return coordenadas_nuevo_evento


def generar_tev(arrow_actual):
    hora_actual = arrow_actual.hour
    coleccion_distr = {
        # Lambda es RATE, SCALE = 1 / LAMBDA
        0: np.random.gamma(shape=0.824484, scale=1 / 0.002855),
        1: np.random.exponential(1 / 0.005502),
        2: np.random.exponential(1 / 0.00725),
        3: np.random.gamma(shape=1.27188, scale=1 / 0.01207),
        4: np.random.exponential(1 / 0.01432),
        5: np.random.exponential(1 / 0.01471),
        6: np.random.gamma(shape=0.82603, scale=1 / 0.01754),
        7: np.random.gamma(shape=0.76578, scale=1 / 0.06982),
        8: np.random.gamma(shape=0.69389, scale=1 / 0.07052),
        9: np.random.gamma(shape=0.62622, scale=1 / 0.06599),
        10: np.random.gamma(shape=0.62801, scale=1 / 0.06811),
        11: np.random.gamma(shape=0.63640, scale=1 / 0.06274),
        12: np.random.gamma(shape=0.66237, scale=1 / 0.06084),
        13: np.random.gamma(shape=0.73307, scale=1 / 0.06331),
        14: np.random.gamma(shape=0.7082, scale=1 / 0.0562),
        15: np.random.gamma(shape=0.77401, scale=1 / 0.05628),
        16: np.random.gamma(shape=0.70061, scale=1 / 0.04434),
        17: np.random.gamma(shape=0.77431, scale=1 / 0.04419),
        18: np.random.gamma(shape=0.77036, scale=1 / 0.02449),
        19: np.random.gamma(shape=0.77329, scale=1 / 0.02159),
        20: np.random.exponential(1 / 0.02225),
        21: np.random.exponential(1 / 0.02002),
        22: np.random.gamma(shape=0.86502, scale=1 / 0.01323),
        23: np.random.gamma(shape=0.90140, scale=1 / 0.01195),
    }

    minutos_entre_llamadas = coleccion_distr[hora_actual]
    return minutos_entre_llamadas


# def calcular_tiempo(mifuncion):
#     start_time = time.time()
#     mifuncion
#     print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    # generar_ubicacion("../datos/eventos.csv")
    fecha_actual = arrow.get('2021-03-02T10:42:00')
    generar_tev(fecha_actual)
    pass
