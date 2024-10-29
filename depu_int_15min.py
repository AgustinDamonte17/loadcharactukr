import os
import pandas as pd
from datetime import timedelta

def depu_int_15min():
    carpeta = r'C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine\CsvPorCostid'
    sufijo = '_depurado.csv'
    
    # Buscar archivos que terminen en _depurado.csv
    for archivo in os.listdir(carpeta):
        if archivo.endswith(sufijo):
            ruta_archivo = os.path.join(carpeta, archivo)
            print(f"Procesando archivo: {archivo}")
            procesar_archivo(ruta_archivo, carpeta)

def procesar_archivo(ruta_archivo, carpeta):
    # Cargar el archivo CSV sin encabezado
    df = pd.read_csv(ruta_archivo, sep=';', header=None)

    # Asegurarse de que las columnas necesarias (A, B, C) sean del tipo correcto
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y-%m-%d', errors='coerce')  # Columna A como fecha
    df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], format='%H:%M', errors='coerce').dt.time  # Columna B como hora (solo HH:MM)
    df.iloc[:, 2] = pd.to_numeric(df.iloc[:, 2], errors='coerce')  # Columna C como numérica (Load)

    # Crear un nuevo DataFrame para almacenar los resultados
    nuevos_datos = []

    # Recorremos cada fila del DataFrame (excepto la última)
    for i in range(len(df) - 1):
        fila_actual = df.iloc[i]
        fila_siguiente = df.iloc[i + 1]

        # Extraer los valores de las columnas A (fecha), B (hora) y C (valor a interpolar)
        fecha_actual = fila_actual[0]  # Fecha de la columna A
        hora_actual = pd.Timestamp.combine(fecha_actual, fila_actual[1])  # Combina fecha y hora actual
        valor_actual = fila_actual[2]  # Valor actual en la columna C
        valor_siguiente = fila_siguiente[2]  # Valor en la columna C de la fila siguiente

        # Añadir la fila original (fecha y hora originales, y valor actual)
        nuevos_datos.append([fecha_actual.strftime('%Y-%m-%d'), fila_actual[1].strftime('%H:%M'), round(valor_actual, 2)])

        # Interpolación lineal para los intervalos de 15 minutos
        intervalo_15min = timedelta(minutes=15)

        # Generamos los bloques de 15 minutos correctamente basados en la hora actual
        for j in range(1, 4):
            nuevo_tiempo = hora_actual + j * intervalo_15min  # Sumar 15, 30, 45 minutos desde la hora actual
            nuevo_valor = valor_actual + j * (valor_siguiente - valor_actual) / 4  # Interpolación lineal

            # Añadir nuevas filas con la misma fecha y la hora interpolada, redondeando a 2 decimales
            nuevos_datos.append([fecha_actual.strftime('%Y-%m-%d'), nuevo_tiempo.strftime('%H:%M'), round(nuevo_valor, 2)])

    # Añadir la última fila sin interpolar (la fila siguiente al último ciclo)
    fecha_ultima = df.iloc[-1, 0].strftime('%Y-%m-%d')
    hora_ultima = df.iloc[-1, 1].strftime('%H:%M')
    valor_ultimo = df.iloc[-1, 2]
    nuevos_datos.append([fecha_ultima, hora_ultima, round(valor_ultimo, 2)])

    # Crear un nuevo DataFrame con los datos procesados
    df_nuevo = pd.DataFrame(nuevos_datos, columns=['Date', 'Time', 'Load (kW)'])

    # Extraer solo el número de custid después de la última aparición de 'costid_'
    base_nombre = os.path.basename(ruta_archivo).replace("_depurado.csv", "")
    custid = base_nombre.split("costid_")[-1]
    nombre_archivo_nuevo = f"profile_for_custid_{custid}.csv"
    ruta_archivo_nuevo = os.path.join(carpeta, nombre_archivo_nuevo)

    # Guardar el nuevo archivo CSV en la misma carpeta
    df_nuevo.to_csv(ruta_archivo_nuevo, sep=';', index=False, header=False)

    print(f"Archivo guardado: {ruta_archivo_nuevo}")
