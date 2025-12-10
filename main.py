#pip install -r requirements.txt

# main.py

from negocio.auth import login, registrar_usuario
from negocio.crud_users import actualizar_usuario, eliminar_usuario
from negocio.crud_todos import crear_todo, actualizar_todo, eliminar_todo
from negocio.negocio_users import obtener_users_api, guardar_users_db
from negocio.negocio_todos import obtener_todos_api, guardar_todos_db

from datos.conexion import session
from sqlalchemy import text
from prettytable import PrettyTable


# ==============================
# FUNCIONES DE VISUALIZACIÓN
# ==============================

def ver_users():
    print("\n=== ACTUALIZANDO USERS DESDE LA API ===")
    users_json = obtener_users_api("https://jsonplaceholder.typicode.com/users")

    if users_json:
        guardar_users_db(users_json)

    # ───────────────────────────────────────────────
    # SOLO UNA TABLA: USERS GUARDADOS EN TU BASE DE DATOS
    # ───────────────────────────────────────────────
    print("\n=== USERS EN BASE DE DATOS (API + TUS REGISTROS) ===")

    rows = session.execute(
        text("SELECT id, name, username, email, phone FROM users ORDER BY id")
    ).fetchall()

    tabla = PrettyTable(["ID", "Nombre", "Username", "Email", "Teléfono"])
    for r in rows:
        tabla.add_row(r)

    print(tabla)


def ver_todos():
    print("\n=== OBTENIENDO TODOS DESDE API ===")
    todos_json = obtener_todos_api("https://jsonplaceholder.typicode.com/todos")

    if todos_json:
        guardar_todos_db(todos_json)

    print("\n=== TODOS EN LA BASE DE DATOS ===")

    rows = session.execute(
        text("SELECT id, userId, title, completed FROM todos ORDER BY id")
    ).fetchall()

    tabla = PrettyTable(["ID", "UserID", "Título", "Completado"])
    for r in rows:
        tabla.add_row([r[0], r[1], r[2], "Sí" if r[3] else "No"])

    print(tabla)


# ==============================
# MENÚ SECUNDARIO (post-login)
# ==============================

def menu_interno():
    while True:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. CRUD USERS")
        print("2. CRUD TODOS")
        print("3. Ver Users")
        print("4. Ver Todos")
        print("5. Cerrar Sesión")

        op = input("Opción: ")

        # SUBMENÚS
        if op == "1":
            menu_users()

        elif op == "2":
            menu_todos()

        # VER DATA
        elif op == "3":
            ver_users()

        elif op == "4":
            ver_todos()

        elif op == "5":
            print("Sesión cerrada.\n")
            return

        else:
            print("❌ Opción inválida\n")


# ==============================
# SUBMENÚ CRUD USERS
# ==============================

def menu_users():
    while True:
        print("\n--- CRUD USERS ---")
        print("1. Actualizar usuario")
        print("2. Eliminar usuario")
        print("3. Volver")

        op = input("Opción: ")

        if op == "1":
            actualizar_usuario()
        elif op == "2":
            eliminar_usuario()
        elif op == "3":
            return
        else:
            print("❌ Opción inválida")


# ==============================
# SUBMENÚ CRUD TODOS
# ==============================

def menu_todos():
    while True:
        print("\n--- CRUD TODOS ---")
        print("1. Crear TODO")
        print("2. Actualizar TODO")
        print("3. Eliminar TODO")
        print("4. Volver")

        op = input("Opción: ")

        if op == "1":
            crear_todo()
        elif op == "2":
            actualizar_todo()
        elif op == "3":
            eliminar_todo()
        elif op == "4":
            return
        else:
            print("❌ Opción inválida")


# ==============================
# MENÚ PRINCIPAL (ANTES DEL LOGIN)
# ==============================

def menu():
    while True:
        print("\n========== SISTEMA ==========")
        print("1. Registrar Usuario")
        print("2. Login")
        print("3. Salir")

        op = input("Opción: ")

        if op == "1":
            registrar_usuario()

        elif op == "2":
            if login():
                menu_interno()

        elif op == "3":
            print("Hasta luego :)")
            break

        else:
            print("❌ Opción inválida")


# ==============================

if __name__ == "__main__":
    menu()
