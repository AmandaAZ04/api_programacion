# negocio/crud_users.py

from sqlalchemy import text
from datos.conexion import session

def actualizar_usuario():
    print("\n=== ACTUALIZAR USUARIO ===")

    user_id = input("ID del usuario: ")

    row = session.execute(
        text("SELECT name, username, email, phone FROM users WHERE id = :id"),
        {"id": user_id}
    ).fetchone()

    if not row:
        print("❌ Usuario no encontrado.")
        return

    new_name = input("Nuevo nombre (enter para mantener): ") or row[0]
    new_username = input("Nuevo username (enter para mantener): ") or row[1]
    new_email = input("Nuevo email (enter para mantener): ") or row[2]
    new_phone = input("Nuevo teléfono (enter para mantener): ") or row[3]

    session.execute(
        text("""
            UPDATE users
            SET name = :n, username = :u, email = :e, phone = :p
            WHERE id = :id
        """),
        {"id": user_id, "n": new_name, "u": new_username, "e": new_email, "p": new_phone}
    )

    session.commit()
    print("✔ Usuario actualizado correctamente")

def eliminar_usuario():
    print("\n=== ELIMINAR USUARIO ===")

    user_id = input("ID del usuario: ")

    # eliminar en tabla usuarios (login)
    session.execute(
        text("""
            DELETE FROM usuarios 
            WHERE username = (SELECT username FROM users WHERE id = :id)
        """),
        {"id": user_id}
    )

    # eliminar en tabla users
    session.execute(
        text("DELETE FROM users WHERE id = :id"),
        {"id": user_id}
    )

    session.commit()
    print("✔ Usuario eliminado")
