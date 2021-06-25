import pandas as pd


def obtener_centros():
    pandas_centros = pd.read_csv("K:/UC/11 semestre/capstone industrial/ICS2122-1-Grupo-14/Simulacion/datos/centros.csv", sep=";")
    numpy_centros = pandas_centros.to_numpy()

    coordenadas_centros = {}
    i = 0
    for centro in numpy_centros:
        coordenadas_centros[f"centro{i}"] = (centro[0], centro[1])
        i += 1

    return coordenadas_centros


def obtener_bases():
    pandas_bases = pd.read_csv("K:/UC/11 semestre/capstone industrial/ICS2122-1-Grupo-14/Simulacion/datos/bases.csv", sep=";")
    numpy_bases = pandas_bases.to_numpy()

    coordenadas_bases = {}
    i = 0
    for base in numpy_bases:
        coordenadas_bases[f"base{i}"] = (base[0], base[1])
        i += 1

    return coordenadas_bases


if __name__ == '__main__':
    print(obtener_bases())
    # print(obtener_centros())
