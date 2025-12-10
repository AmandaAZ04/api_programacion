from sqlalchemy import text
from datos.conexion import session
from servicios.api_client import APIClient

client = APIClient("https://jsonplaceholder.typicode.com")

def crear_todo():
    print("\n=== CREAR TODO ===")

    userId = input("UserID: ").strip()
    title = input("Título: ").strip()
    completed_input = input("¿Completado? (s/n): ").lower().strip()

    # VALIDACIONES
    # Validar userId no vacío
    if not userId:
        print("Recurso no creado: falta UserID.")
        return

    # Validar que userId sea número
    if not userId.isdigit():
        print("Recurso no creado: UserID debe ser un número.")
        return

    # Validar título no vacío
    if not title:
        print("Recurso no creado: falta Título.")
        return

    # Validar completado
    if completed_input not in ("s", "n"):
        print("Recurso no creado: respuesta inválida en 'completado'.")
        return

    completed = completed_input == "s"

    # SI todo ES VÁLIDO, CONTINUAMOS
    data = {
        "userId": int(userId),
        "title": title,
        "completed": completed
    }

    # Intento de creación en API
    resp = client.post("/todos", data)

    # Manejo de error en API
    if not resp["ok"]:
        print(f"Error en API: {resp['error']}")
        return

    # Guardar en BD con ID incremental
    row = session.execute(text("SELECT MAX(id) FROM todos")).fetchone()
    next_id = (row[0] or 0) + 1

    session.execute(
        text("""
            INSERT INTO todos (id, userId, title, completed)
            VALUES (:id, :u, :t, :c)
        """),
        {"id": next_id, "u": userId, "t": title, "c": completed}
    )
    session.commit()

    print("TODO creado correctamente en API + BD")


def actualizar_todo():
    print("\n=== ACTUALIZAR TODO ===")
    todo_id = input("ID: ")

    title = input("Nuevo título: ")
    completed = input("¿Completado? (s/n): ").lower() == "s"

    resp = client.put(f"/todos/{todo_id}", {"title": title, "completed": completed})

    session.execute(
        text("""
            UPDATE todos
            SET title = :t, completed = :c
            WHERE id = :id
        """),
        {"id": todo_id, "t": title, "c": completed}
    )
    session.commit()

    print("Actualizado en API + BD")

def eliminar_todo():
    print("\n=== ELIMINAR TODO ===")
    todo_id = input("ID: ")

    resp = client.delete(f"/todos/{todo_id}")

    session.execute(
        text("DELETE FROM todos WHERE id = :id"),
        {"id": todo_id}
    )
    session.commit()

    print("Eliminado en API + BD")
