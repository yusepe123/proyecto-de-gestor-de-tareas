import json
import os

RUTA_CARPETA = "datos"
RUTA_ARCHIVO = "datos/tareas.json"

def cargar_datos():
    if not os.path.exists(RUTA_CARPETA):
        os.makedirs(RUTA_CARPETA, exist_ok=True)
        
    if not os.path.exists(RUTA_ARCHIVO):
        return []
        
    try:
        with open(RUTA_ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(tareas):
    if not os.path.exists(RUTA_CARPETA):
        os.makedirs(RUTA_CARPETA, exist_ok=True)
        
    try:
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(tareas, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f">> Error al intentar guardar los datos: {e}")