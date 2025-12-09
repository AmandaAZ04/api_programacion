import requests
from prettytable import PrettyTable
from datos.conexion import session
from modelos.modelos import Todo

# -------------------------------------------------------
# GET TODOS desde API
# -------------------------------------------------------
def obtener_todos_api(url):
    tabla = PrettyTable()
    tabla.field_names = ['ID', 'UserID', 'Título', 'Completado']

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Error al obtener todos:", e)
        return None

    todos_json = resp.json()

    for t in todos_json:
        tabla.add_row([
            t["id"],
            t["userId"],
            t["title"],
            "Sí" if t["completed"] else "No"
        ])

    print(tabla)
    return todos_json


# -------------------------------------------------------
# Guardar TODOS en BD
# -------------------------------------------------------
def guardar_todos_db(todos_json):
    if not todos_json:
        print("No hay tareas para guardar.")
        return

    for t in todos_json:
        data = {
            "id": t["id"],
            "userId": t["userId"],
            "title": t["title"],
            "completed": bool(t["completed"])
        }

        session.merge(Todo(**data))

    session.commit()
    print("Todos guardados en la base de datos correctamente.")
