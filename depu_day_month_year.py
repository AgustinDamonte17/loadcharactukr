import pandas as pd
import os

def depu_day_month_year(csv_file_path):
    """
    Lee el archivo CSV generado a partir del XLSX, transforma los datos en la columna C
    que están en formato 'YYYY-MM-DD HH:MM:SS.mmmmmm' o 'YYYY-MM-DD HH:MM:SS' al formato estándar
    'YYYY-MM-DD HH:MM:SS', y los coloca en la columna D. Si el dato ya está en el formato estándar, lo copia sin modificaciones.
    Si los minutos y segundos son '59:59', redondea a la siguiente hora.
    """
    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path, header=None, dtype=str, sep=';', encoding='utf-8')

    # Verificar que la columna C existe (índice 2)
    if 2 not in df.columns:
        print("La columna C no existe en el archivo.")
        return

    # Crear una lista para almacenar los nuevos valores de la columna D
    new_column_d = []

    # Iterar sobre cada valor en la columna C
    for idx, value in df[2].items():
        if pd.isna(value):
            new_value = ''
        else:
            value = value.strip()
            try:
                # Intentar parsear el valor con el formato 'YYYY-MM-DD HH:MM:SS.mmmmmm'
                dt = pd.to_datetime(value, format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
                if pd.isna(dt):
                    # Si falla, intentar parsear con el formato 'YYYY-MM-DD HH:MM:SS'
                    dt = pd.to_datetime(value, format='%Y-%m-%d %H:%M:%S', errors='coerce')
                if pd.isna(dt):
                    # Si aún falla, copiar el valor tal cual
                    new_value = value
                else:
                    # Si los minutos y segundos son 59:59, redondear a la siguiente hora
                    if dt.minute == 59 and dt.second == 59:
                        dt = dt + pd.Timedelta(hours=1)
                        dt = dt.replace(minute=0, second=0)
                    
                    # Convertir al formato estándar 'YYYY-MM-DD HH:MM:SS'
                    new_value = dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                # En caso de error, copiar el valor tal cual
                new_value = value

        # Agregar el nuevo valor a la lista
        new_column_d.append(new_value)

    # Agregar la nueva columna D al DataFrame
    df[3] = new_column_d  # Columna D (índice 3)

    # Generar una copia del archivo CSV con las modificaciones
    dir_name, base_name = os.path.split(csv_file_path)
    name, ext = os.path.splitext(base_name)
    new_csv_file_path = os.path.join(dir_name, f"{name}_depurado.csv")

    # Guardar el DataFrame modificado en el nuevo archivo CSV
    df.to_csv(new_csv_file_path, index=False, header=False, sep=';', encoding='utf-8')

    print(f"Archivo depurado y guardado: {new_csv_file_path}")

    # Devolver la ruta del nuevo archivo CSV para su uso posterior
    return new_csv_file_path
