from sqlalchemy import text
from datos.conexion import session
from negocio.encriptacion import Encriptador
import stdiomask

enc = Encriptador()

def login():
    print("\n--- LOGIN ---")

    username = input("Usuario: ")
    password = stdiomask.getpass("Contraseña: ")

    row = session.execute(
        text("SELECT contrasena, sal FROM usuarios WHERE username = :u"),
        {"u": username}
    ).fetchone()

    if not row:
        print("✘ Usuario no encontrado.\n")
        return False

    hash_guardado, salt = row

    if enc.comparar(password, salt, hash_guardado):
        print("✔ Login exitoso.\n")
        return True
    else:
        print("✘ Contraseña incorrecta.\n")
        return False


def registrar_usuario():
    print("\n--- REGISTRO DE USUARIO ---")

    name = input("Nombre completo: ")
    username = input("Username: ")
    email = input("Email: ")
    phone = input("Teléfono: ")
    password = stdiomask.getpass("Contraseña: ")

    salt = enc.generar_salt()
    hash_pwd = enc.encriptar(password, salt)

    row = session.execute(text("SELECT MAX(id) FROM users")).fetchone()
    next_id = (row[0] or 0) + 1

    # INSERT users
    session.execute(
        text("""
            INSERT INTO users (id, name, username, email, phone, website)
            VALUES (:id, :n, :u, :e, :p, '')
        """),
        {"id": next_id, "n": name, "u": username, "e": email, "p": phone}
    )

    # INSERT usuarios (login)
    session.execute(
        text("""
            INSERT INTO usuarios (username, email, contrasena, sal)
            VALUES (:u, :e, :c, :s)
        """),
        {"u": username, "e": email, "c": hash_pwd, "s": salt}
    )

    session.commit()
    print("\n✔ Usuario registrado correctamente.\n")
