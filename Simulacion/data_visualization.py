import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot

if __name__ == '__main__':
    tablas_finales_25 = pd.read_csv(f"./entrega3/resultados_finales/25%_diario.csv", sep=";")
    tablas_finales_50 = pd.read_csv(f"./entrega3/resultados_finales/50%_diario.csv", sep=";")
    tablas_finales_75 = pd.read_csv(f"./entrega3/resultados_finales/75%_diario.csv", sep=";")
    tablas_finales_85 = pd.read_csv(f"./entrega3/resultados_finales/85%_diario.csv", sep=";")
    tablas_finales_95 = pd.read_csv(f"./entrega3/resultados_finales/95%_diario.csv", sep=";")
    tablas_finales_mean = pd.read_csv(f"./entrega3/resultados_finales/mean_diario.csv", sep=";")
    tablas_iniciales_95 = pd.read_csv(f"./entrega3/resultados_iniciales/95%_diario.csv", sep=";")
    # print((conjunto_tablas[0]['TIEMPO_PROCESO'].rename("UNO")))

    data_preproc = pd.DataFrame({
        'DIA': tablas_iniciales_95["DIA"],
        '0': tablas_iniciales_95['TIEMPO_PROCESO'],
        '1': tablas_finales_95['TIEMPO_PROCESO'],
        # '2': conjunto_tablas[2]['TIEMPO_PROCESO'],
        # '3': conjunto_tablas[3]['TIEMPO_PROCESO'],
        # '4': conjunto_tablas[4]['TIEMPO_PROCESO'],
        # '5': conjunto_tablas[5]['TIEMPO_PROCESO'],
        # '6': conjunto_tablas[6]['TIEMPO_PROCESO'],
        # '7': conjunto_tablas[7]['TIEMPO_PROCESO'],
    })
    detalle_final = pd.DataFrame({
        'DIA': tablas_iniciales_95["DIA"],
        'MEAN': tablas_finales_mean['TIEMPO_PROCESO'],
        '25%': tablas_finales_25['TIEMPO_PROCESO'],
        '50%': tablas_finales_50['TIEMPO_PROCESO'],
        '75%': tablas_finales_75['TIEMPO_PROCESO'],
        '85%': tablas_finales_85['TIEMPO_PROCESO'],
        '95%': tablas_finales_95['TIEMPO_PROCESO'],
    })

    sns.lineplot(x='DIA', y='Minutos', hue='variable',
                 data=pd.melt(detalle_final, ['DIA'], value_name="Minutos"))

    pyplot.show()
