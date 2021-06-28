import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot

if __name__ == '__main__':
    conjunto_tablas = [pd.read_csv(f"./entrega3/v6 comparacion mclp inicial/{core}/95%_diario.csv", sep=";") for core in range(8)]
    print((conjunto_tablas[0]['TIEMPO_PROCESO'].rename("UNO")))

    data_preproc = pd.DataFrame({
        'DIA': conjunto_tablas[0]["DIA"],
        '0': conjunto_tablas[0]['TIEMPO_PROCESO'],
        '1': conjunto_tablas[1]['TIEMPO_PROCESO'],
        '2': conjunto_tablas[2]['TIEMPO_PROCESO'],
        '3': conjunto_tablas[3]['TIEMPO_PROCESO'],
        '4': conjunto_tablas[4]['TIEMPO_PROCESO'],
        '5': conjunto_tablas[5]['TIEMPO_PROCESO'],
        '6': conjunto_tablas[6]['TIEMPO_PROCESO'],
        '7': conjunto_tablas[7]['TIEMPO_PROCESO'],
    })

    sns.lineplot(x='DIA', y='Minutos', hue='variable',
                 data=pd.melt(data_preproc, ['DIA'], value_name="Minutos"))

    pyplot.show()
