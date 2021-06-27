import pandas as pd
import numpy as np
import sys
from random import randint
import seaborn as sns
import matplotlib.pyplot as plt
import time


# def alterar_atencion():
#     pandas_eventos = pd.read_csv("./datos/eventos.csv", sep=";")
#     numpy_eventos = pandas_eventos.to_numpy()
#     solo_atenciones = [(evento[4] - 4.2) for evento in numpy_eventos]
#     pd.DataFrame(solo_atenciones).to_csv(path_or_buf=f"datos modificados/solo_atenciones_desplazadas.csv", index=False, header=["NEWATENCION"], sep=";")


def filtrar_muestra():
    pandas_muestra = pd.read_csv("./datos/muestraSGED.csv", sep=",")
    df_filtrados = pandas_muestra.loc[pandas_muestra['x'] <= 46.7]
    df_filtrados.to_csv(path_or_buf=f"datos/muestraSGEDfiltrada.csv", index=False, header=["Atenciones"], sep=";")


def filtrar_despacho():
    pandas_muestra = pd.read_csv("./datos/muestraDespacho.csv", sep=",")
    df_filtrados = pandas_muestra.loc[pandas_muestra['x'] <= 14.5]
    df_filtrados.to_csv(path_or_buf=f"datos/muestraDespachofiltrada.csv", index=False, header=["Atenciones"], sep=";")


def filtrar_derivacion():
    pandas_muestra = pd.read_csv("./datos/muestraDerivacion.csv", sep=",")
    df_filtrados = pandas_muestra.loc[pandas_muestra['x'] <= 31]
    df_filtrados.to_csv(path_or_buf=f"datos/muestraDerivacionfiltrada.csv", index=False, header=["Atenciones"], sep=";")


def random_sged():
    pandas_muestra = pd.read_csv("./datos/muestraSGEDfiltrada.csv", sep=",")
    numpy_filtrados = pandas_muestra.to_numpy()
    lista_filtrado = [atencion[0] for atencion in numpy_filtrados]
    random_atencion = lista_filtrado[randint(0, len(lista_filtrado) - 1)]
    return random_atencion


def agregar_clusters():
    pandas_eventos = pd.read_csv("./datos/eventos.csv", sep=";")
    pandas_eventos_clusters = pd.read_csv("./datos/eventos_clusterizados.csv", sep=";")

    numpy_eventos_clusters = pandas_eventos_clusters.to_numpy()
    numpy_eventos = pandas_eventos.to_numpy()

    lista_clusters = []
    for evento in numpy_eventos_clusters:
        lista_clusters.append(evento[2])

    lista_horas = []
    lista_dias = []
    dia = 1
    ultima_hora = 0
    for idx, evento in enumerate(numpy_eventos):
        hora = int(evento[2][0:2])
        minutos = int(evento[2][3:])
        minutos_totales = hora * 60 + minutos
        lista_horas.append(minutos_totales)

        if hora < ultima_hora:
            dia += 1
            ultima_hora = hora
            lista_dias.append(dia)

        else:
            lista_dias.append(dia)
            ultima_hora = hora

    pandas_eventos["CLUSTER"] = lista_clusters
    pandas_eventos["HORARIO_EN_MINUTOS"] = lista_horas
    pandas_eventos["DIA"] = lista_dias

    pandas_eventos.to_csv(path_or_buf=f"datos modificados/eventos_cluster_minutos_dias.csv", index=False, sep=";")
    for i in range(1, 10):
        este_panda_cluster = pandas_eventos.loc[pandas_eventos['CLUSTER'] == i]
        este_panda_cluster.to_csv(path_or_buf=f"datos modificados/eventos_cluster{i}_minutos_dias.csv", index=False, sep=";")


def obtener_tiempo_entre_eventos():
    # bloques_horarios = {
    #     1: [],  # 03;00 - 06;59  min
    #     2: [],  # 07;00 - 07;59  min
    #     3: [],  # 08;00 - 10;59  min
    #     4: [],  # 11;00 - 17;59  min
    #     5: [],  # 18;00 - 19;59  min
    #     6: [],  # 20;00 - 22;59  min
    #     7: [],  # 23;00 - 02;59  min
    # }

    bloques_horarios = {}
    for i in range(24):
        bloques_horarios[i] = []

    # pandas_eventos = pd.read_csv("./datos modificados/eventos_cluster1_minutos_dias.csv", sep=";")
    pandas_eventos = pd.read_csv("./datos modificados/eventos_cluster_minutos_dias.csv", sep=";")
    numpy_eventos = pandas_eventos.to_numpy()
    ultimo_minuto = None

    for evento in numpy_eventos:
        minuto_actual = evento[7]
        if not ultimo_minuto:
            ultimo_minuto = minuto_actual
            continue

        if minuto_actual < ultimo_minuto:
            tiempo_entre_eventos = (minuto_actual + 1440) - ultimo_minuto

        else:
            tiempo_entre_eventos = minuto_actual - ultimo_minuto
            if tiempo_entre_eventos == 0:
                tiempo_entre_eventos = 0.0001

        if ultimo_minuto < (60 * 1):
            bloques_horarios[0].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 2):
            bloques_horarios[1].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 3):
            bloques_horarios[2].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 4):
            bloques_horarios[3].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 5):
            bloques_horarios[4].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 6):
            bloques_horarios[5].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 7):
            bloques_horarios[6].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 8):
            bloques_horarios[7].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 9):
            bloques_horarios[8].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 10):
            bloques_horarios[9].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 11):
            bloques_horarios[10].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 12):
            bloques_horarios[11].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 13):
            bloques_horarios[12].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 14):
            bloques_horarios[13].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 15):
            bloques_horarios[14].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 16):
            bloques_horarios[15].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 17):
            bloques_horarios[16].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 18):
            bloques_horarios[17].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 19):
            bloques_horarios[18].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 20):
            bloques_horarios[19].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 21):
            bloques_horarios[20].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 22):
            bloques_horarios[21].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 23):
            bloques_horarios[22].append(tiempo_entre_eventos)
        elif ultimo_minuto < (60 * 24):
            bloques_horarios[23].append(tiempo_entre_eventos)

        ultimo_minuto = minuto_actual

    for i in range(0, 24):
        df = pd.DataFrame(bloques_horarios[i], columns=[f'TEV'])
        df.to_csv(path_or_buf=f"./datos finales/tev{i}.csv", index=False, sep=";")

    return


if __name__ == '__main__':
    # agregar_clusters()
    # obtener_tiempo_entre_eventos()
    # alterar_atencion()
    pass
