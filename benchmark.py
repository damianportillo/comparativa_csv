import time
import psutil
import os
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt

# función para merdir el rendimiento del tiempo de ejecución
# y memoria usada durante la ejecución de una función
def medir_rendimiento(funcion, *args, **kwargs):
    proceso = psutil.Process(os.getpid())

    # Memoria antes
    memoria_antes = proceso.memory_info().rss / (1024 ** 2)  

    # Tiempo de inicio
    inicio = time.perf_counter()

    resultado = funcion(*args, **kwargs)

    # Tiempo de fin
    fin = time.perf_counter()

    # Memoria después
    memoria_despues = proceso.memory_info().rss / (1024 ** 2)  

    tiempo_total = fin - inicio
    memoria_usada = memoria_despues - memoria_antes

    return resultado, tiempo_total, memoria_usada

# función para impotar informacion de un archivo formato csv
# usando la libreria pandas
def cargar_con_pandas(ruta_csv):
    df = pd.read_csv(ruta_csv)
    print("\n[Pandas] Primeras filas:")
    print(df.head())
    return df

# función para impotar informacion de un archivo formato csv
# usando la libreria polars
def cargar_con_polars(ruta_csv):
    df = pl.read_csv(ruta_csv)
    print("\n[Polars] Primeras filas:")
    print(df.head())
    return df

# bloque de ejecucón principal del programa
if __name__ == '__main__':
    archivo = "train_split_00.csv"

    # Medición
    _, tiempo_pandas, memoria_pandas = medir_rendimiento(cargar_con_pandas, archivo)
    _, tiempo_polars, memoria_polars = medir_rendimiento(cargar_con_polars, archivo)

    # Mostrar resultados
    print("\n--- Resultados ---")
    print(f"Pandas - Tiempo: {tiempo_pandas:.4f} s | Memoria: {memoria_pandas:.2f} MiB")
    print(f"Polars - Tiempo: {tiempo_polars:.4f} s | Memoria: {memoria_polars:.2f} MiB")

    # Gráfico
    etiquetas = ['Pandas', 'Polars']
    tiempos = [tiempo_pandas, tiempo_polars]
    memorias = [memoria_pandas, memoria_polars]

    plt.figure(figsize=(10, 5))

    # Tiempo
    plt.subplot(1, 2, 1)
    plt.bar(etiquetas, tiempos, color=['blue', 'green'])
    plt.title('Tiempo de Ejecución')
    plt.ylabel('Segundos')

    # Memoria
    plt.subplot(1, 2, 2)
    plt.bar(etiquetas, memorias, color=['blue', 'green'])
    plt.title('Uso de Memoria')
    plt.ylabel('MiB')

    plt.suptitle('Benchmark Preciso: Pandas vs Polars')
    plt.tight_layout()
    plt.show()
