from datetime import datetime
from persistencia import guardar_datos

# --- FUNCIONES DE VALIDACIÓN ---

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print(">> Error: Este campo no puede quedar vacío.")

def pedir_prioridad():
    while True:
        print("Seleccione la prioridad: [1] Alta | [2] Media | [3] Baja")
        try:
            opcion = int(input("Opción (1-3): ").strip())
            if opcion == 1:
                return "Alta"
            elif opcion == 2:
                return "Media"
            elif opcion == 3:
                return "Baja"
            else:
                print(">> Error: Elija un número entre 1 y 3.")
        except ValueError:
            print(">> Error: Debe ingresar un número entero válido (1, 2 o 3).")

def pedir_estado():
    while True:
        print("Seleccione el estado: [1] Pendiente | [2] Completada")
        try:
            opcion = int(input("Opción (1-2): ").strip())
            if opcion == 1:
                return "Pendiente"
            elif opcion == 2:
                return "Completada"
            else:
                print(">> Error: Elija 1 o 2.")
        except ValueError:
            print(">> Error: Debe ingresar un número entero (1 o 2).")

def pedir_fecha(mensaje):
    while True:
        fecha_texto = input(mensaje).strip()
        try:
            # Validamos que exista en el calendario con formato DD/MM/AAAA
            datetime.strptime(fecha_texto, "%d/%m/%Y")
            return fecha_texto
        except ValueError:
            print(">> Error: Fecha inválida. Use el formato DD/MM/AAAA (ejemplo: 15/11/2026).")


# --- FUNCIONES DEL SISTEMA (CRUD Y REPORTE) ---

def registrar_tarea(tareas):
    print("\n--- REGISTRAR NUEVA TAREA ---")
    titulo = pedir_texto("Título de la tarea: ")
    
    for t in tareas:
        if t["titulo"].lower() == titulo.lower():
            print(">> Error: Ya existe una tarea registrada con ese título.")
            return

    prioridad = pedir_prioridad()
    fecha_limite = pedir_fecha("Fecha límite (DD/MM/AAAA): ")
    # Por defecto toda tarea nueva inicia como Pendiente
    estado = "Pendiente"

    nueva_tarea = {
        "titulo": titulo,
        "prioridad": prioridad,
        "estado": estado,
        "fecha_limite": fecha_limite
    }

    tareas.append(nueva_tarea)
    guardar_datos(tareas)
    print(f">> Tarea '{titulo}' registrada como Pendiente.")


def listar_tareas(tareas):
    print("\n--- LISTA DE TAREAS REGISTRADAS ---")
    if len(tareas) == 0:
        print("No hay tareas registradas todavía.")
        return

    print(f"{'#':<4} {'Título':<26} {'Prioridad':<12} {'Estado':<14} {'Fecha Límite':<12}")
    print("-" * 70)
    for i, t in enumerate(tareas, start=1):
        print(f"{i:<4} {t['titulo']:<26} {t['prioridad']:<12} {t['estado']:<14} {t['fecha_limite']:<12}")


def buscar_tarea(tareas):
    print("\n--- BUSCAR TAREA ---")
    if len(tareas) == 0:
        print("No hay tareas registradas.")
        return

    termino = pedir_texto("Ingrese título, prioridad o estado a buscar: ").lower()
    encontradas = []

    for t in tareas:
        if (termino in t["titulo"].lower() or 
            termino in t["prioridad"].lower() or 
            termino in t["estado"].lower()):
            encontradas.append(t)

    if len(encontradas) > 0:
        print(f"\nSe encontraron {len(encontradas)} coincidencia(s):")
        for t in encontradas:
            print(f"- {t['titulo']} | Prioridad: {t['prioridad']} | Estado: {t['estado']} | Límite: {t['fecha_limite']}")
    else:
        print(">> No se encontró ninguna tarea con ese criterio.")


def modificar_tarea(tareas):
    print("\n--- MODIFICAR TAREA ---")
    if len(tareas) == 0:
        print("No hay tareas registradas.")
        return

    listar_tareas(tareas)
    try:
        indice = int(input("\nIngrese el número (#) de la tarea a modificar: ").strip()) - 1
        if indice < 0 or indice >= len(tareas):
            print(">> Error: Número de tarea fuera de rango.")
            return
    except ValueError:
        print(">> Error: Debe ingresar un número entero válido.")
        return

    t = tareas[indice]
    print(f"\nModificando: '{t['titulo']}' (Prioridad: {t['prioridad']}, Estado: {t['estado']}, Fecha: {t['fecha_limite']})")
    print("1. Cambiar título")
    print("2. Cambiar prioridad")
    print("3. Cambiar estado (Pendiente / Completada)")
    print("4. Cambiar fecha límite")
    print("5. Cancelar")
    
    opcion = input("Seleccione una opción (1-5): ").strip()
    
    if opcion == "1":
        t["titulo"] = pedir_texto("Nuevo título: ")
    elif opcion == "2":
        t["prioridad"] = pedir_prioridad()
    elif opcion == "3":
        t["estado"] = pedir_estado()
    elif opcion == "4":
        t["fecha_limite"] = pedir_fecha("Nueva fecha límite (DD/MM/AAAA): ")
    elif opcion == "5":
        print("Modificación cancelada.")
        return
    else:
        print(">> Opción no válida.")
        return

    guardar_datos(tareas)
    print(">> Tarea actualizada correctamente.")


def eliminar_tarea(tareas):
    print("\n--- ELIMINAR TAREA ---")
    if len(tareas) == 0:
        print("No hay tareas registradas.")
        return

    listar_tareas(tareas)
    try:
        indice = int(input("\nIngrese el número (#) de la tarea a eliminar: ").strip()) - 1
        if indice < 0 or indice >= len(tareas):
            print(">> Error: Número de tarea no existe.")
            return
    except ValueError:
        print(">> Error: Debe ingresar un número entero válido.")
        return

    tarea_elegida = tareas[indice]
    confirmacion = input(f"¿Seguro que desea eliminar '{tarea_elegida['titulo']}'? (s/n): ").strip().lower()
    if confirmacion == "s":
        eliminada = tareas.pop(indice)
        guardar_datos(tareas)
        print(f">> La tarea '{eliminada['titulo']}' fue eliminada del sistema.")
    else:
        print("Operación cancelada.")


def generar_reporte(tareas):
    print("\n--- REPORTE: TAREAS PENDIENTES POR PRIORIDAD ---")
    if len(tareas) == 0:
        print("No hay tareas registradas para generar el reporte.")
        return

    pendientes = [t for t in tareas if t["estado"] == "Pendiente"]
    completadas = len(tareas) - len(pendientes)

    print(f"Total de tareas registradas: {len(tareas)}")
    print(f"Tareas completadas: {completadas} | Tareas pendientes: {len(pendientes)}")

    if len(pendientes) == 0:
        print("\n¡Felicidades! No tienes ninguna tarea pendiente.")
        return

    for nivel in ["Alta", "Media", "Baja"]:
        filtradas = [t for t in pendientes if t["prioridad"] == nivel]
        print(f"\nPrioridad {nivel.upper()} ({len(filtradas)}):")
        if len(filtradas) > 0:
            for t in filtradas:
                print(f"  [ ] {t['titulo']} (Fecha límite: {t['fecha_limite']})")
        else:
            print("  Ninguna tarea pendiente en esta prioridad.")