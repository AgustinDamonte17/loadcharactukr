import os

def encontrar_archivos_xlsx():
    ruta = r'C:\Users\adamonte\Desktop\AGUSTIN\Python\LoadCharacterizationUkraine'
    archivos_xlsx = [f for f in os.listdir(ruta) if f.endswith('.xlsx')]
    return [os.path.join(ruta, f) for f in archivos_xlsx]
