from datetime import datetime, date


class Task:
    def __init__(self, title, description="", priority="Medium", due_date=None):
        self.title = title
        self.description = description
        self.priority = priority  # High, Medium, Low
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None

    def mark_completed(self):
        """Marcar la tarea como completada"""
        self.completed = True
        self.completed_at = datetime.now()

    def __str__(self):
        status = "[COMPLETADA]" if self.completed else "[PENDIENTE]"
        due_str = f" | Vence: {self.due_date}" if self.due_date else ""
        return f"{status} {self.title} | Prioridad: {self.priority}{due_str}"


class TodoListManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, description="", priority="Medium", due_date=None):
        """Agregar una nueva tarea a la lista"""
        task = Task(title, description, priority, due_date)
        self.tasks.append(task)
        print(f"Tarea agregada exitosamente: '{title}'")
        self.next_id += 1

    def list_tasks(self):
        """Mostrar todas las tareas"""
        if not self.tasks:
            print("No hay tareas en la lista.")
            return

        print("\nLista de tareas:")
        print("=" * 80)
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")
            if task.description:
                print(f"   Descripción: {task.description}")
            print(f"   Creada: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            if task.completed and task.completed_at:
                print(f"   Completada: {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 80)

    def list_tasks_detailed(self):
        """Mostrar todas las tareas con detalles completos"""
        if not self.tasks:
            print("No hay tareas en la lista.")
            return

        print("\nLista detallada de tareas:")
        print("=" * 80)
        for i, task in enumerate(self.tasks, 1):
            status = "COMPLETADA" if task.completed else "PENDIENTE"
            print(f"ID: {i}")
            print(f"Título: {task.title}")
            print(f"Descripción: {task.description if task.description else 'Sin descripción'}")
            print(f"Prioridad: {task.priority}")
            print(f"Fecha límite: {task.due_date if task.due_date else 'Sin fecha límite'}")
            print(f"Estado: {status}")
            print(f"Creada: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.completed and task.completed_at:
                print(f"Completada: {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)

    def mark_completed(self, task_number):
        """Marcar una tarea como completada"""
        if 1 <= task_number <= len(self.tasks):
            task = self.tasks[task_number - 1]
            if task.completed:
                print(f"La tarea '{task.title}' ya está completada.")
            else:
                task.mark_completed()
                print(f"Tarea '{task.title}' marcada como completada.")
        else:
            print(f"Número de tarea inválido. Debe ser entre 1 y {len(self.tasks)}")

    def list_by_priority(self, priority):
        """Listar tareas por prioridad"""
        filtered_tasks = [task for task in self.tasks if task.priority.lower() == priority.lower()]
        if not filtered_tasks:
            print(f"No hay tareas con prioridad '{priority}'.")
            return

        print(f"\nTareas con prioridad '{priority}':")
        print("-" * 60)
        for i, task in enumerate(filtered_tasks, 1):
            status = "[COMPLETADA]" if task.completed else "[PENDIENTE]"
            print(f"{i}. {status} {task.title}")
            if task.description:
                print(f"   Descripción: {task.description}")
        print("-" * 60)

    def list_pending_tasks(self):
        """Listar solo las tareas pendientes"""
        pending_tasks = [task for task in self.tasks if not task.completed]
        if not pending_tasks:
            print("No hay tareas pendientes.")
            return

        print("\nTareas pendientes:")
        print("-" * 60)
        for i, task in enumerate(pending_tasks, 1):
            due_str = f" | Vence: {task.due_date}" if task.due_date else ""
            print(f"{i}. {task.title} | Prioridad: {task.priority}{due_str}")
            if task.description:
                print(f"   Descripción: {task.description}")
        print("-" * 60)


def get_priority():
    """Obtener la prioridad de la tarea del usuario"""
    while True:
        print("\nSelecciona la prioridad:")
        print("1. Alta")
        print("2. Media")
        print("3. Baja")
        choice = input("Ingresa tu opción (1-3) o presiona Enter para 'Media': ").strip()

        if choice == '1':
            return "High"
        elif choice == '2' or choice == '':
            return "Medium"
        elif choice == '3':
            return "Low"
        else:
            print("Opción inválida. Por favor, selecciona 1, 2 o 3.")


def get_due_date():
    """Obtener la fecha límite de la tarea del usuario"""
    while True:
        date_input = input("Ingresa la fecha límite (YYYY-MM-DD) o presiona Enter para omitir: ").strip()
        if not date_input:
            return None

        try:
            due_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            if due_date < date.today():
                print("La fecha límite no puede ser en el pasado.")
                continue
            return due_date
        except ValueError:
            print("Formato de fecha inválido. Usa YYYY-MM-DD (ejemplo: 2024-12-31)")


def show_menu():
    """Mostrar el menú de opciones"""
    print("\n" + "=" * 60)
    print("TO-DO LIST MANAGER")
    print("=" * 60)
    print("1. Agregar nueva tarea")
    print("2. Listar todas las tareas")
    print("3. Listar tareas con detalles")
    print("4. Marcar tarea como completada")
    print("5. Listar tareas pendientes")
    print("6. Listar tareas por prioridad")
    print("7. Salir")
    print("=" * 60)


def main():
    todo_manager = TodoListManager()

    print("¡Bienvenido al Gestor de Lista de Tareas!")

    while True:
        show_menu()

        try:
            choice = input("Selecciona una opción (1-7): ").strip()

            if choice == '1':
                print("\n--- Agregar nueva tarea ---")
                title = input("Título de la tarea: ").strip()
                if not title:
                    print("El título no puede estar vacío.")
                    continue

                description = input("Descripción (opcional): ").strip()
                priority = get_priority()
                due_date = get_due_date()

                todo_manager.add_task(title, description, priority, due_date)

            elif choice == '2':
                todo_manager.list_tasks()

            elif choice == '3':
                todo_manager.list_tasks_detailed()

            elif choice == '4':
                if not todo_manager.tasks:
                    print("No hay tareas para marcar como completadas.")
                else:
                    todo_manager.list_tasks()
                    try:
                        task_num = int(input("Ingresa el número de la tarea a completar: "))
                        todo_manager.mark_completed(task_num)
                    except ValueError:
                        print("Por favor, ingresa un número válido.")

            elif choice == '5':
                todo_manager.list_pending_tasks()

            elif choice == '6':
                priority = input("Ingresa la prioridad (High/Medium/Low): ").strip()
                if priority.lower() in ['high', 'medium', 'low']:
                    todo_manager.list_by_priority(priority)
                else:
                    print("Prioridad inválida. Usa: High, Medium, o Low")

            elif choice == '7':
                print("¡Hasta luego! Gracias por usar el Gestor de Tareas.")
                break

            else:
                print("Opción inválida. Por favor, selecciona una opción del 1 al 7.")

        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! Programa terminado.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()