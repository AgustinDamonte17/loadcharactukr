import os
import pandas as pd
from xlsx_to_csv import convertir_xlsx_a_csv
from depu_day_month_year import depu_day_month_year
from day_month_year_id import day_month_year_id
from sep_csv_costid import sep_csv_costid
from depurar_archivos_csv import depurar_archivos_csv
from depu_int_15min import depu_int_15min  # Importamos la nueva función

def xlsx_finder():
    ruta = r'C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine'
    archivos_xlsx = [f for f in os.listdir(ruta) if f.endswith('.xlsx')]
    return [os.path.join(ruta, f) for f in archivos_xlsx]

if __name__ == "__main__":    
    archivos = xlsx_finder()
    if not archivos:
        print("No se encontraron archivos .xlsx para procesar.")
    else:
        for archivo in archivos:
            try:
                print(f"Procesando archivo: {archivo}")

                # Leer el archivo .xlsx en un DataFrame
                df = pd.read_excel(archivo, header=None, dtype=str)

                # Definir la ruta para el archivo CSV
                dir_name, base_name = os.path.split(archivo)
                name, ext = os.path.splitext(base_name)
                archivo_csv = os.path.join(dir_name, f"{name}.csv")

                # Convertir el DataFrame a CSV usando convertir_xlsx_a_csv
                convertir_xlsx_a_csv(df, archivo_csv)

                print(f"Archivo convertido exitosamente: {archivo_csv}")

                # Llamar a la función depu_day_month_year
                archivo_csv_depurado = depu_day_month_year(archivo_csv)

                # Llamar a la función day_month_year_id con el archivo depurado
                day_month_year_id(archivo_csv_depurado)

                print(f"Archivo procesado y modificado exitosamente: {archivo_csv_depurado}")

                # Llamar a la función sep_csv_costid para dividir por Costid
                sep_csv_costid()  # Asegúrate de que esta función crea la carpeta correctamente

                print(f"Archivos CSV por Costid generados exitosamente para: {archivo_csv_depurado}")

                # Llamar a la función depurar_archivos_csv para depurar los archivos generados
                depurar_archivos_csv()

                print("Archivos depurados exitosamente.")

                # Llamar a la nueva función para procesar los CSV en intervalos de 15 minutos
                carpeta_csv = r"C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine\CsvPorCostid"
                depu_int_15min()

                print("Archivos convertidos a intervalos de 15 minutos exitosamente.")

            except Exception as e:
                print(f"Error al procesar el archivo {archivo}: {e}\n")
        
        print("Conversión y procesamiento completados para todos los archivos.")
