import requests
from prettytable import PrettyTable
from datos.conexion import session
from modelos.modelos import User

# GET USERS desde API
def obtener_users_api(url):
    tabla = PrettyTable()
    tabla.field_names = ['ID', 'Nombre', 'Usuario', 'Email', 'Teléfono']

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Error al obtener users:", e)
        return None

    users_json = resp.json()

    for u in users_json:
        tabla.add_row([
            u["id"],
            u["name"],
            u["username"],
            u["email"],
            u.get("phone", "")
        ])

    print(tabla)
    return users_json

# Guardar USERS en BD
def guardar_users_db(users_json):
    if not users_json:
        print("No hay users para guardar")
        return

    for u in users_json:
        data = {
            "id": u["id"],
            "name": u["name"],
            "username": u["username"],
            "email": u["email"],
            "phone": u.get("phone", None),
            "website": u.get("website", None)
        }

        # merge = inserta si no existe / actualiza si existe
        session.merge(User(**data))

    session.commit()
    print("Usuarios guardados en la base de datos correctamente")