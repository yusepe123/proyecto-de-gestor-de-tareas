from persistencia import cargar_datos
import logica

def mostrar_menu():
    print("\n==========================================")
    print("        SISTEMA GESTOR DE TAREAS          ")
    print("==========================================")
    print("1. Registrar nueva tarea")
    print("2. Listar todas las tareas")
    print("3. Buscar tarea")
    print("4. Modificar tarea (o marcar completada)")
    print("5. Eliminar tarea")
    print("6. Ver reporte de pendientes por prioridad")
    print("7. Salir")
    print("==========================================")

def main():
    tareas = cargar_datos()
    
    while True:
        mostrar_menu()
        opcion = input("Elija una opción (1-7): ").strip()

        if opcion == "1":
            logica.registrar_tarea(tareas)
        elif opcion == "2":
            logica.listar_tareas(tareas)
        elif opcion == "3":
            logica.buscar_tarea(tareas)
        elif opcion == "4":
            logica.modificar_tarea(tareas)
        elif opcion == "5":
            logica.eliminar_tarea(tareas)
        elif opcion == "6":
            logica.generar_reporte(tareas)
        elif opcion == "7":
            print("\nGuardando cambios y saliendo del gestor... ¡Hasta luego!")
            break
        else:
            print("\n>> Opción inválida. Por favor seleccione un número del 1 al 7.")

if __name__ == "__main__":
    main()