import pandas as pd
import csv
import os

def convertir_xlsx_a_csv(df, ruta_csv):
    # Abrir el archivo CSV para escritura
    with open(ruta_csv, 'w', encoding='utf-8', newline='') as csvfile:
        # Crear un objeto writer de csv con los parámetros adecuados
        csv_writer = csv.writer(
            csvfile,
            delimiter=';',           # Usar ';' como separador de campos
            quotechar='"',           # Usar comillas dobles para encerrar los campos
            quoting=csv.QUOTE_ALL,   # Encerrar todos los campos entre comillas
            escapechar='\\'          # Carácter de escape para caracteres especiales
        )

        # Iterar sobre las filas del DataFrame y escribirlas en el archivo CSV
        for index, row in df.iterrows():
            # Obtener los valores de la fila como lista
            row_data = row.tolist()
            # Escribir la fila en el archivo CSV
            csv_writer.writerow(row_data)

    print(f"Archivo convertido y guardado: {ruta_csv}")
