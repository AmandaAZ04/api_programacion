#pip install -r requirements.txt

from servicios.api_client import APIClient
from negocio.encriptacion import Encriptador
from negocio.negocio_users import obtener_users_api, guardar_users_db
from negocio.negocio_todos import obtener_todos_api, guardar_todos_db
from datos.conexion import session
from modelos.modelos import Base, User, Todo
from sqlalchemy.exc import SQLAlchemyError

# ----------------------------------------------------
# CONFIGURACIÓN API
# ----------------------------------------------------
API_BASE = "https://jsonplaceholder.typicode.com"
client = APIClient(API_BASE)
enc = Encriptador()


# ----------------------------------------------------
# Crear tablas si no existen
# ----------------------------------------------------
def crear_tablas():
    from datos.conexion import engine
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas / verificadas correctamente.\n")
    except Exception as e:
        print("Error al crear tablas:", e)


# ----------------------------------------------------
# REGISTRO DE USUARIO
# ----------------------------------------------------
def registrar_usuario():
    from sqlalchemy import text
    print("\n--- Registro de Usuario ---")

    username = input("Usuario: ")
    email = input("Email: ")
    password = input("Contraseña: ")

    # encriptación
    salt = enc.generar_salt()
    hash_pwd = enc.encriptar(password, salt)

    try:
        session.execute(
            text("INSERT INTO usuarios (username, email, contrasena, sal) VALUES (:u, :e, :c, :s)"),
            {"u": username, "e": email, "c": hash_pwd, "s": salt}
        )
        session.commit()
        print("Usuario registrado correctamente.\n")
    except SQLAlchemyError as e:
        print("Error registrando usuario:", e)


# ----------------------------------------------------
# LOGIN DE USUARIO
# ----------------------------------------------------
def login():
    print("\n--- Login ---")

    username = input("Usuario: ")
    password = input("Contraseña: ")

    try:
        row = session.execute(
            "SELECT contrasena, sal FROM usuarios WHERE username = :u",
            {"u": username}
        ).fetchone()

        if not row:
            print("Usuario no encontrado.\n")
            return False

        hash_guardado = row[0]
        salt = row[1]

        if enc.comparar(password, salt, hash_guardado):
            print("Login exitoso.\n")
            return True
        else:
            print("Contraseña incorrecta.\n")
            return False

    except SQLAlchemyError as e:
        print("Error en login:", e)
        return False


# ----------------------------------------------------
# GET USERS → BD
# ----------------------------------------------------
def opcion_obtener_users():
    print("\n--- Obtener Users desde API ---")
    users_json = obtener_users_api(f"{API_BASE}/users")
    if users_json:
        guardar_users_db(users_json)


# ----------------------------------------------------
# GET TODOS → BD
# ----------------------------------------------------
def opcion_obtener_todos():
    print("\n--- Obtener Todos desde API ---")
    todos_json = obtener_todos_api(f"{API_BASE}/todos")
    if todos_json:
        guardar_todos_db(todos_json)


# ----------------------------------------------------
# POST (crear elemento)
# ----------------------------------------------------
def opcion_post():
    print("\n--- Crear recurso (POST) ---")
    title = input("Título: ")
    body = input("Contenido: ")
    userId = input("User ID: ")

    data = {
        "title": title,
        "body": body,
        "userId": userId
    }

    resp = client.post("/posts", data)
    print("Respuesta POST:", resp)


# ----------------------------------------------------
# PUT (actualizar elemento)
# ----------------------------------------------------
def opcion_put():
    print("\n--- Actualizar recurso (PUT) ---")
    post_id = input("ID del post a actualizar: ")
    title = input("Nuevo título: ")
    body = input("Nuevo contenido: ")

    data = {
        "id": post_id,
        "title": title,
        "body": body
    }

    resp = client.put(f"/posts/{post_id}", data)
    print("Respuesta PUT:", resp)


# ----------------------------------------------------
# DELETE
# ----------------------------------------------------
def opcion_delete():
    print("\n--- Eliminar recurso (DELETE) ---")
    post_id = input("ID del post a eliminar: ")

    resp = client.delete(f"/posts/{post_id}")
    print("Respuesta DELETE:", resp)


# ----------------------------------------------------
# MENU PRINCIPAL
# ----------------------------------------------------
def menu():
    crear_tablas()

    print("\n===== SISTEMA CON POO & API =====\n")

    while True:
        print("1. Registrar Usuario")
        print("2. Login")
        print("3. Obtener Users (GET → BD)")
        print("4. Obtener Todos (GET → BD)")
        print("5. Crear recurso (POST)")
        print("6. Actualizar recurso (PUT)")
        print("7. Eliminar recurso (DELETE)")
        print("8. Salir")

        opcion = input("\nSeleccione opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            login()
        elif opcion == "3":
            opcion_obtener_users()
        elif opcion == "4":
            opcion_obtener_todos()
        elif opcion == "5":
            opcion_post()
        elif opcion == "6":
            opcion_put()
        elif opcion == "7":
            opcion_delete()
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")


# ----------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------------------
if __name__ == "__main__":
    menu()
