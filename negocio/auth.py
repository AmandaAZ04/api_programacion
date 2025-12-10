from sqlalchemy import text
from datos.conexion import session
from negocio.encriptacion import Encriptador
import stdiomask

from negocio.validaciones import (
    validar_nombre,
    validar_email,
    validar_telefono,
    validar_username,
    validar_no_vacio
)

enc = Encriptador()

def login():
    print("\n--- LOGIN ---")

    # 1) VALIDAR QUE EL USUARIO EXISTA EN TABLA USERS
    while True:
        username = input("Usuario: ")

        if not validar_no_vacio(username, "Usuario"):
            continue

        # Buscar username en tabla users de la API/local
        row_user = session.execute(
            text("SELECT id, username FROM users WHERE username = :u"),
            {"u": username}
        ).fetchone()

        if row_user:
            print("Usuario encontrado\n")
            break
        else:
            print("Ese usuario NO existe en la tabla USERS")
            print("   Intente nuevamente\n")

    # 2) BUSCAR CONTRASEÑA DEL USUARIO EN TABLA USUARIOS
    row_login = session.execute(
        text("SELECT contrasena, sal FROM usuarios WHERE username = :u"),
        {"u": username}
    ).fetchone()

    if not row_login:
        print("Este usuario existe en USERS pero no tiene contraseña registrada")
        print("Regístrelo primero\n")
        return False

    hash_guardado, salt = row_login

    # 3) VALIDAR CONTRASEÑA (pedir hasta que sea correcta)
    while True:
        password = stdiomask.getpass("Contraseña: ")

        if not validar_no_vacio(password, "Contraseña"):
            continue

        if enc.comparar(password, salt, hash_guardado):
            print("Login exitoso\n")
            return True
        else:
            print("Contraseña incorrecta. Intente nuevamente\n")

# REGISTRO DE USUARIO (CON VALIDACIONES COMPLETAS)
def registrar_usuario():
    print("\n--- REGISTRO DE USUARIO ---")

    # VALIDAR NOMBRE COMPLETO
    while True:
        name = input("Nombre completo: ")
        if validar_nombre(name):
            break

    # VALIDAR USERNAME
    while True:
        username = input("Username: ")
        if validar_username(username):
            break

    # VALIDAR EMAIL
    while True:
        email = input("Email: ")
        if validar_email(email):
            break

    # VALIDAR TELÉFONO
    while True:
        phone = input("Teléfono: ")
        if validar_telefono(phone):
            break

    # VALIDAR CONTRASEÑA
    while True:
        password = stdiomask.getpass("Contraseña: ")
        if validar_no_vacio(password, "Contraseña"):
            break

    # HASH + SAL
    salt = enc.generar_salt()
    hash_pwd = enc.encriptar(password, salt)

    # GENERAR NUEVO ID
    row = session.execute(text("SELECT MAX(id) FROM users")).fetchone()
    next_id = (row[0] or 0) + 1

    try:
        # GUARDAR EN TABLA USERS
        session.execute(
            text("""
                INSERT INTO users (id, name, username, email, phone, website)
                VALUES (:id, :n, :u, :e, :p, '')
            """),
            {"id": next_id, "n": name, "u": username, "e": email, "p": phone}
        )

        # GUARDAR EN TABLA USUARIOS (LOGIN)
        session.execute(
            text("""
                INSERT INTO usuarios (username, email, contrasena, sal)
                VALUES (:u, :e, :c, :s)
            """),
            {"u": username, "e": email, "c": hash_pwd, "s": salt}
        )

        session.commit()
        print("\n✔ Usuario registrado correctamente.\n")

    except Exception as e:
        print("✘ Error registrando usuario:", e)