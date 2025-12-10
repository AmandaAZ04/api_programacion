from sqlalchemy import text
from datos.conexion import session
from servicios.api_client import APIClient

client = APIClient("https://jsonplaceholder.typicode.com")

def crear_todo():
    print("\n--- CREAR TODO ---")

    userId = input("UserID: ")
    title = input("Título: ")
    completed = input("¿Completado? (s/n): ").lower() == "s"

    data = {"userId": int(userId), "title": title, "completed": completed}

    resp = client.post("/todos", data)
    if resp["ok"]:
        print("✔ Creado en API")
    else:
        print(f"✘ Error API: {resp['status']} → {resp['error']}")

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
    print("✔ Guardado en BD.")


def actualizar_todo():
    print("\n--- ACTUALIZAR TODO ---")

    todo_id = input("ID: ")
    title = input("Nuevo título: ")
    completed = input("¿Completado? (s/n): ").lower() == "s"

    resp = client.put(f"/todos/{todo_id}", {"title": title, "completed": completed})

    if resp["ok"]:
        print("✔ Actualizado en API")
    else:
        print(f"✘ Error API: {resp['status']} → {resp['error']}")

    session.execute(
        text("""
            UPDATE todos
            SET title = :t, completed = :c
            WHERE id = :id
        """),
        {"id": todo_id, "t": title, "c": completed}
    )
    session.commit()
    print("✔ Actualizado en BD.")


def eliminar_todo():
    print("\n--- ELIMINAR TODO ---")

    todo_id = input("ID: ")

    resp = client.delete(f"/todos/{todo_id}")
    if resp["ok"]:
        print("✔ Eliminado en API")
    else:
        print(f"✘ Error API: {resp['status']} → {resp['error']}")

    session.execute(
        text("DELETE FROM todos WHERE id = :id"),
        {"id": todo_id}
    )
    session.commit()
    print("✔ Eliminado de BD.")
