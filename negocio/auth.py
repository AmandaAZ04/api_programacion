from sqlalchemy import text
from datos.conexion import session
from negocio.encriptacion import Encriptador
import stdiomask
from negocio.validaciones import (validar_nombre, validar_username, validar_email, validar_telefono, validar_no_vacio)

enc = Encriptador()

def login():
    print("\n=== LOGIN ===")

    # Ver si existe en USERS
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
            print("Ese usuario no existe")
            return False

    # Buscar contraseña en tabla USUARIOS
    row_login = session.execute(
        text("SELECT contrasena, sal FROM usuarios WHERE username = :u"),
        {"u": username}
    ).fetchone()

    if not row_login:
        print("Este usuario no tiene contraseña registrada.")
        return False

    hash_guardado, salt = row_login

    # Verificar contraseña
    while True:
        password = stdiomask.getpass("Contraseña: ")

        if not validar_no_vacio(password, "Contraseña"):
            continue

        if enc.comparar(password, salt, hash_guardado):
            print("Login exitoso.\n")
            return True
        else:
            print("Contraseña incorrecta.\n")

def registrar_usuario():
    print("\n=== REGISTRO DE USUARIO ===")

    # VALIDACIONES DEL NOMBRE
    while True:
        name = input("Nombre completo: ")
        if validar_nombre(name):
            break

    # USERNAME
    while True:
        username = input("Username: ")
        if validar_username(username):
            break

    # EMAIL
    while True:
        email = input("Email: ")
        if validar_email(email):
            break

    # TELÉFONO
    while True:
        phone = input("Teléfono: ")
        if validar_telefono(phone):
            break

    # CONTRASEÑA ENMASCARADA
    while True:
        password = stdiomask.getpass("Contraseña: ")
        if validar_no_vacio(password, "Contraseña"):
            break

    # ENCRIPTACIÓN
    salt = enc.generar_salt()
    hash_pwd = enc.encriptar(password, salt)

    # OBTENER SIGUIENTE ID
    row = session.execute(text("SELECT MAX(id) FROM users")).fetchone()
    next_id = (row[0] or 0) + 1

    # INSERTAR EN USERS
    try:
        session.execute(
            text("""
                INSERT INTO users (id, name, username, email, phone, website)
                VALUES (:id, :n, :u, :e, :p, '')
            """),
            {"id": next_id, "n": name, "u": username, "e": email, "p": phone}
        )

        # INSERTAR EN USUARIOS (LOGIN)
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
        print("Error registrando usuario:", e)
        return

    # MOSTRAR TABLA COMPLETA: USERS DE API + USUARIOS REGISTRADOS POR TI
    print("=== USERS ACTUALIZADOS (API + TUS REGISTROS) ===")

    rows = session.execute(
        text("SELECT id, name, username, email, phone FROM users ORDER BY id")
    ).fetchall()

    from prettytable import PrettyTable
    tabla = PrettyTable(["ID", "Nombre", "Username", "Email", "Teléfono"])

    for r in rows:
        tabla.add_row([r[0], r[1], r[2], r[3], r[4]])

    print(tabla)