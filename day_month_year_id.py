import pandas as pd
import os

def day_month_year_id(csv_file_path):
    """
    Procesa el archivo .csv especificado, agregando el día de la semana en inglés,
    mes, año, hora y la fecha en formato YYYY-MM-DD a cada línea de datos, a partir de la columna D.
    """
    # Leer el archivo CSV sin modificar los valores originales
    df = pd.read_csv(csv_file_path, header=None, dtype=str, sep=';', encoding='utf-8')

    # Función para procesar cada fila
    def process_row(row):
        # Obtener una lista de los valores originales de la fila
        row_values = row.values.tolist()

        # Asegurarnos de que la fila tenga al menos 4 elementos
        while len(row_values) < 4:
            row_values.append('')

        # Asumiendo que la cadena de fecha y hora está en la cuarta columna (índice 3)
        date_time_str = row_values[3]

        # Verificar que date_time_str no sea NaN o vacío
        if pd.isna(date_time_str) or date_time_str.strip() == '':
            date_str = ''
            time_str = ''
        else:
            date_time_str = date_time_str.strip()
            # Separar la fecha y la hora
            if '  ' in date_time_str:
                date_str, time_str = date_time_str.split('  ', 1)
            else:
                # Manejar casos con uno o más espacios
                parts = date_time_str.strip().split()
                if len(parts) >= 2:
                    date_str = parts[0]
                    time_str = parts[1]
                elif len(parts) == 1:
                    date_str = parts[0]
                    time_str = ''
                else:
                    date_str = ''
                    time_str = ''

        # Limpiar date_str eliminando caracteres no deseados
        date_str = date_str.strip()

        # Inicializar variables
        date_obj = None
        day_of_week = ''
        month_number = ''
        year_number = ''
        formatted_date = ''  # Nueva variable para la fecha en formato YYYY-MM-DD

        # Intentar parsear la fecha usando diferentes formatos
        formatos_fecha = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
        for formato in formatos_fecha:
            try:
                date_obj = pd.to_datetime(date_str, format=formato, errors='raise')
                break  # Si se parsea correctamente, salir del bucle
            except Exception:
                continue  # Intentar con el siguiente formato

        # Si la fecha se parseó correctamente
        if date_obj is not None:
            # Obtener el nombre del día de la semana en inglés
            day_of_week = date_obj.strftime('%A')
            month_number = str(date_obj.month)
            year_number = str(date_obj.year)
            # Obtener la fecha en formato YYYY-MM-DD
            formatted_date = date_obj.strftime('%Y-%m-%d')
        else:
            # Mostrar mensaje de error para depuración
            print(f"Error al parsear la fecha en la fila {row.name}: '{date_str}'")

        # Crear una nueva fila sin modificar los valores originales
        new_row = row_values.copy()

        # Añadir los nuevos valores al final de la fila
        new_row.extend([day_of_week, month_number, year_number, time_str, formatted_date])

        return new_row

    # Procesar cada fila del DataFrame y obtener una lista de filas procesadas
    processed_rows = df.apply(process_row, axis=1).tolist()

    # Determinar el número máximo de columnas para asegurar consistencia
    max_columns = max(len(row) for row in processed_rows)

    # Crear un nuevo DataFrame con las filas procesadas y el número correcto de columnas
    df_processed = pd.DataFrame(processed_rows, columns=range(max_columns))

    # Generar la ruta para el nuevo archivo CSV
    dir_name, base_name = os.path.split(csv_file_path)
    name, ext = os.path.splitext(base_name)
    new_csv_file_path = os.path.join(dir_name, f"{name}_modificado.csv")

    # Guardar el DataFrame procesado en el nuevo archivo CSV sin modificar los datos originales
    df_processed.to_csv(new_csv_file_path, index=False, header=False, sep=';', encoding='utf-8', quoting=3)

    print(f"Archivo procesado y guardado: {new_csv_file_path}")
