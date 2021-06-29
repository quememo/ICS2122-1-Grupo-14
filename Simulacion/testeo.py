import pandas as pd


def calcular_porcentaje(inicial, final):
    return ((final - inicial) / inicial) * 100


if __name__ == '__main__':
    # print(calcular_porcentaje(213.91856290692502, 204.02003248884049))
    # superDict = {1: pd.DataFrame([[1, 1], [1, 1, ]], columns=["MINUTOS", "DIAS"], index=['mean', 'sd']),
    #              2: pd.DataFrame([[2, 2], [2, 2, ]], columns=["MINUTOS", "DIAS"], index=['mean', 'sd'])}
    #
    # print(min(superDict, key=superDict.get['MINUTOS']['mean']))

    diccionario = {
        7: "hola",
        1: "hola",
        3: "ESTE NO ES",
        0: "hola",
        5: "hola",
        4: "hola",
        2: "que sarpa",
        6: "hola",
    }

    funciona_pls = diccionario.pop(2)
    print(funciona_pls)
    print(diccionario)
