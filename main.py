#pip install -r requirements.txt

from negocio.auth import login, registrar_usuario
from negocio.crud_users import actualizar_usuario, eliminar_usuario
from negocio.crud_todos import crear_todo, actualizar_todo, eliminar_todo
from negocio.negocio_users import obtener_users_api, guardar_users_db
from negocio.negocio_todos import obtener_todos_api, guardar_todos_db
from datos.conexion import session
from sqlalchemy import text


def ver_users():
    users_json = obtener_users_api("https://jsonplaceholder.typicode.com/users")
    if users_json:
        guardar_users_db(users_json)

    rows = session.execute(
        text("SELECT id, name, username, email, phone FROM users ORDER BY id")
    ).fetchall()

    from prettytable import PrettyTable
    tabla = PrettyTable()
    tabla.field_names = ["ID", "Nombre", "Username", "Email", "Teléfono"]

    for r in rows:
        tabla.add_row(r)

    print(tabla)


def ver_todos():
    todos_json = obtener_todos_api("https://jsonplaceholder.typicode.com/todos")
    if todos_json:
        guardar_todos_db(todos_json)

    rows = session.execute(
        text("SELECT id, userId, title, completed FROM todos ORDER BY id")
    ).fetchall()

    from prettytable import PrettyTable
    tabla = PrettyTable()
    tabla.field_names = ["ID", "UserID", "Título", "Completado"]

    for r in rows:
        tabla.add_row([r[0], r[1], r[2], "Sí" if r[3] else "No"])

    print(tabla)


def menu():
    while True:
        print("\n===== SISTEMA ORDENADO =====")
        print("1. Login")
        print("2. Registrar Usuario")

        print("\n--- CRUD USERS ---")
        print("3. Actualizar Usuario")
        print("4. Eliminar Usuario")

        print("\n--- CRUD TODOS ---")
        print("5. Crear TODO")
        print("6. Actualizar TODO")
        print("7. Eliminar TODO")

        print("\n--- VER DATOS ---")
        print("8. Ver Users")
        print("9. Ver Todos")

        print("\n10. Salir")

        op = input("Opción: ")

        if op == "1": login()
        elif op == "2": registrar_usuario()
        elif op == "3": actualizar_usuario()
        elif op == "4": eliminar_usuario()
        elif op == "5": crear_todo()
        elif op == "6": actualizar_todo()
        elif op == "7": eliminar_todo()
        elif op == "8": ver_users()
        elif op == "9": ver_todos()
        elif op == "10": break
        else: print("Opción inválida.")


if __name__ == "__main__":
    menu()
