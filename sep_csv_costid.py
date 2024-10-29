import os
import pandas as pd

def sep_csv_costid():
    """
    Toma el archivo CSV 'Inputpromedidores_depurado_modificado.csv', identifica los registros que comparten el mismo Costid (columna A o con nombre Costid),
    y genera un archivo CSV separado para cada Costid en una carpeta llamada 'csv por costid'.
    """
    # Definir la ruta al archivo CSV 'Inputpromedidores_depurado_modificado.csv'
    csv_file_path = r'C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine\Inputpromedidores_depurado_modificado.csv'

    # Leer el archivo CSV, tratando de inferir si hay encabezados
    try:
        df = pd.read_csv(csv_file_path, dtype=str, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Verificar si el archivo tiene encabezados imprimiendo las primeras filas
    print("Primeras filas del archivo CSV para revisión:")
    print(df.head())

    # Verificar si la primera fila parece ser encabezado, es decir, si el archivo tiene nombres de columnas
    if 'Costid' in df.columns:
        costid_column = 'Costid'  # El archivo tiene encabezados, y la columna Costid tiene este nombre
    else:
        costid_column = df.columns[0]  # Usamos el primer índice como Costid si no hay encabezados

    print(f"Usando la columna '{costid_column}' como Costid")

    # Crear la carpeta 'csv por costid' en la misma ruta del archivo CSV
    dir_name, base_name = os.path.split(csv_file_path)
    output_dir = os.path.join(dir_name, 'CsvPorCostid')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Carpeta creada: {output_dir}")

    # Iterar sobre cada Costid único en la columna identificada
    unique_costids = df[costid_column].unique()  # Obtener valores únicos de Costid
    for costid in unique_costids:
        # Filtrar los datos que corresponden al Costid actual
        df_costid = df[df[costid_column] == costid]

        # Definir el nombre del nuevo archivo CSV para este Costid
        output_file_path = os.path.join(output_dir, f"inputpromedidores_costid_{costid}.csv")

        # Guardar el DataFrame filtrado en el nuevo archivo CSV
        df_costid.to_csv(output_file_path, index=False, sep=';', encoding='utf-8')

        print(f"Archivo creado para Costid {costid}: {output_file_path}")

    print("Todos los archivos CSV por Costid han sido generados correctamente.")
