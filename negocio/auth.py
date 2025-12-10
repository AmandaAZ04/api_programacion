# negocio/auth.py

from sqlalchemy import text
from datos.conexion import session
from negocio.encriptacion import Encriptador
import stdiomask
from negocio.validaciones import (
    validar_nombre, validar_username, validar_email,
    validar_telefono, validar_no_vacio
)

enc = Encriptador()

# ==========================
# LOGIN
# ==========================

def login():
    print("\n=== LOGIN ===")

    # 1) Ver si existe en USERS
    while True:
        username = input("Usuario: ")

        if not validar_no_vacio(username, "Usuario"):
            continue

        row_user = session.execute(
            text("SELECT id FROM users WHERE username = :u"),
            {"u": username}
        ).fetchone()

        if row_user:
            break
        else:
            print("❌ Ese usuario no existe en USERS.")
            return False

    # 2) Buscar contraseña en tabla USUARIOS
    row_login = session.execute(
        text("SELECT contrasena, sal FROM usuarios WHERE username = :u"),
        {"u": username}
    ).fetchone()

    if not row_login:
        print("❌ Este usuario no tiene contraseña registrada.")
        return False

    hash_guardado, salt = row_login

    # 3) Verificar contraseña
    while True:
        password = stdiomask.getpass("Contraseña: ")

        if not validar_no_vacio(password, "Contraseña"):
            continue

        if enc.comparar(password, salt, hash_guardado):
            print("✔ Login exitoso.\n")
            return True
        else:
            print("❌ Contraseña incorrecta.\n")

# ==========================
# REGISTRO
# ==========================

def registrar_usuario():
    print("\n=== REGISTRO DE USUARIO ===")

    # VALIDACIONES
    while True:
        name = input("Nombre completo: ")
        if validar_nombre(name):
            break

    while True:
        username = input("Username: ")
        if validar_username(username):
            break

    while True:
        email = input("Email: ")
        if validar_email(email):
            break

    while True:
        phone = input("Teléfono: ")
        if validar_telefono(phone):
            break

    while True:
        password = stdiomask.getpass("Contraseña: ")
        if validar_no_vacio(password, "Contraseña"):
            break

    salt = enc.generar_salt()
    hash_pwd = enc.encriptar(password, salt)

    # GENERAR ID AUTOMÁTICO
    row = session.execute(text("SELECT MAX(id) FROM users")).fetchone()
    next_id = (row[0] or 0) + 1

    # GUARDAR USERS
    try:
        session.execute(
            text("""
                INSERT INTO users (id, name, username, email, phone, website)
                VALUES (:id, :n, :u, :e, :p, '')
            """),
            {"id": next_id, "n": name, "u": username, "e": email, "p": phone}
        )

        # GUARDAR USUARIOS (login)
        session.execute(
            text("""
                INSERT INTO usuarios (username, email, contrasena, sal)
                VALUES (:u, :e, :c, :s)
            """),
            {"u": username, "e": email, "c": hash_pwd, "s": salt}
        )

        session.commit()
        print("✔ Usuario registrado correctamente.\n")

    except Exception as e:
        print("❌ Error registrando usuario:", e)
