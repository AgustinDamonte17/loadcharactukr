import os
import pandas as pd

def depurar_archivos_csv():
    """
    Depura todos los archivos CSV en la carpeta 'csv por costid', creando nuevos archivos con los encabezados:
    Fecha, Hora y KWH. Los datos se toman de las columnas I, H y B respectivamente de los archivos originales.
    
    Los nuevos archivos serán guardados con el sufijo "_depurado" en la misma carpeta.
    """
    
    ruta_carpeta = r'C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine\CsvPorCostid'

    # Verificar si la carpeta 'csv por costid' existe
    if not os.path.exists(ruta_carpeta):
        raise FileNotFoundError(f"La carpeta especificada no existe: {ruta_carpeta}")

    # Iterar sobre todos los archivos en la carpeta
    for archivo in os.listdir(ruta_carpeta):
        # Verificar que el archivo sea un CSV
        if archivo.endswith('.csv'):
            archivo_csv = os.path.join(ruta_carpeta, archivo)

            # Leer el archivo CSV original
            df = pd.read_csv(archivo_csv, sep=';', dtype=str, encoding='utf-8')

            # Verificar si el archivo tiene suficientes columnas (al menos hasta la columna I)
            if df.shape[1] >= 9:  # Debemos asegurarnos que tiene al menos hasta la columna I (índice 8)
                # Crear un nuevo DataFrame con las columnas requeridas
                df_nuevo = pd.DataFrame({
                    'Fecha': df.iloc[:, 8],  # Columna I
                    'Hora': pd.to_datetime(df.iloc[:, 7]).dt.strftime('%H:%M'),   # Columna H, ajustando el formato a HH:MM
                    'KWH': df.iloc[:, 1].astype(float).round(2)  # Columna B, formateada a dos decimales
                })

                # Definir el nombre del nuevo archivo CSV depurado
                nombre_archivo, extension = os.path.splitext(archivo)
                nuevo_nombre_archivo = f"{nombre_archivo}_depurado.csv"
                ruta_nuevo_archivo = os.path.join(ruta_carpeta, nuevo_nombre_archivo)

                # Guardar el nuevo DataFrame en el archivo CSV depurado sin encabezados y con el separador ;
                df_nuevo.to_csv(ruta_nuevo_archivo, index=False, sep=';', encoding='utf-8', header=False)

                print(f"Archivo depurado guardado: {ruta_nuevo_archivo}")
            else:
                print(f"El archivo {archivo} no tiene suficientes columnas para procesar.")
