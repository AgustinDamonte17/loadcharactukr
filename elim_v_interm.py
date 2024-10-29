import os

def elim_v_interm():
    carpeta = r'C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine\CsvPorCostid'
    prefijo = 'inputpromedidores'
    
    # Verificar si la carpeta existe antes de intentar acceder prueba cambio
    if not os.path.exists(carpeta):
        print(f"La carpeta especificada no existe: {carpeta}")
        return

    # Listar y eliminar archivos en la carpeta que coincidan con el prefijo
    for archivo in os.listdir(carpeta):
        if archivo.startswith(prefijo) and archivo.endswith('.csv'):
            ruta_archivo = os.path.join(carpeta, archivo)
            os.remove(ruta_archivo)
            print(f"Archivo eliminado: {ruta_archivo}")
