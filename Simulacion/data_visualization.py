import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot

if __name__ == '__main__':
    # INICIALES
    tablas_iniciales_25 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_iniciales/25%_diario.csv", sep=";")
    tablas_iniciales_50 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_iniciales/50%_diario.csv", sep=";")
    tablas_iniciales_75 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_iniciales/75%_diario.csv", sep=";")
    tablas_iniciales_85 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_iniciales/85%_diario.csv", sep=";")
    tablas_iniciales_95 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_iniciales/95%_diario.csv", sep=";")
    tablas_iniciales_mean = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_iniciales/mean_diario.csv", sep=";")

    # FINALES
    tablas_finales_25 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_finales/25%_diario.csv", sep=";")
    tablas_finales_50 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_finales/50%_diario.csv", sep=";")
    tablas_finales_75 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_finales/75%_diario.csv", sep=";")
    tablas_finales_85 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_finales/85%_diario.csv", sep=";")
    tablas_finales_95 = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_finales/95%_diario.csv", sep=";")
    tablas_finales_mean = pd.read_csv(f"./resultados finales/comparacion algoritmo recursivo/resultados_finales/mean_diario.csv", sep=";")

    inicial_proceso_percentiles = pd.DataFrame({
        'Dia': tablas_iniciales_mean["DIA"],
        'Promedio': tablas_iniciales_mean['TIEMPO_PROCESO'],
        'Percentil 25%': tablas_iniciales_25['TIEMPO_PROCESO'],
        'Percentil 50%': tablas_iniciales_50['TIEMPO_PROCESO'],
        'Percentil 75%': tablas_iniciales_75['TIEMPO_PROCESO'],
        'Percentil 85%': tablas_iniciales_85['TIEMPO_PROCESO'],
        'Percentil 95%': tablas_iniciales_95['TIEMPO_PROCESO'],
    })

    inicial_desglose_tiempos_95 = pd.DataFrame({
        'Dia': tablas_iniciales_95["DIA"],
        'Espera en cola': tablas_iniciales_95['TIEMPO_ATRASO'],
        'Despacho': tablas_iniciales_95['TIEMPO_DESPACHO'],
        'Traslado hacia emergencia': tablas_iniciales_95['TIEMPO_IDA'],
        'Atención prehospitalaria': tablas_iniciales_95['TIEMPO_ATENCION'],
        'Traslado hacia centro': tablas_iniciales_95['TIEMPO_TRASLADO'],
        'Derivacion': tablas_iniciales_95['TIEMPO_DERIVACION'],
        'Proceso completo': tablas_iniciales_95['TIEMPO_PROCESO'],
    })

    versus = pd.DataFrame({
        'Dia': tablas_iniciales_95["DIA"],
        'Asignación Inicial': tablas_iniciales_95['TIEMPO_PROCESO'],
        'Asignación Eficiente': tablas_finales_95['TIEMPO_PROCESO'],
    })

    sns.relplot(x='Dia', y='Minutos', hue='Tiempos de proceso', kind="line", height=6, aspect=2,
                data=pd.melt(versus, ['Dia'], value_name="Minutos", var_name="Tiempos de proceso"))

    pyplot.show()
