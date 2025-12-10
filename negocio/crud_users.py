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
        print("Usuario no encontrado.")
        return

    # Mostrar valores actuales y solicitar nuevos
    print("\nValores actuales:")
    print(f"Nombre: {row[0]}")
    print(f"Username: {row[1]}")
    print(f"Email: {row[2]}")
    print(f"Teléfono: {row[3]}\n")

    new_name = input("Nuevo nombre (enter para mantener): ") or row[0]
    new_username = input("Nuevo username (enter para mantener): ") or row[1]
    new_email = input("Nuevo email (enter para mantener): ") or row[2]
    new_phone = input("Nuevo teléfono (enter para mantener): ") or row[3]

    # Actualizar en BD
    session.execute(
        text("""
            UPDATE users
            SET name = :n, username = :u, email = :e, phone = :p
            WHERE id = :id
        """),
        {
            "id": user_id,
            "n": new_name,
            "u": new_username,
            "e": new_email,
            "p": new_phone
        }
    )

    session.commit()
    print("\nUsuario actualizado correctamente.\n")

    # MOSTRAR TABLA ACTUALIZADA
    print("=== USERS ACTUALIZADOS (API + TUS REGISTROS) ===")

    rows = session.execute(
        text("SELECT id, name, username, email, phone FROM users ORDER BY id")
    ).fetchall()

    from prettytable import PrettyTable
    tabla = PrettyTable(["ID", "Nombre", "Username", "Email", "Teléfono"])

    for r in rows:
        tabla.add_row([r[0], r[1], r[2], r[3], r[4]])

    print(tabla)


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
    print("Usuario eliminado")