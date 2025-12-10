# negocio/validaciones.py

import re

def validar_no_vacio(valor, nombre_campo):
    if not valor.strip():
        print(f"❌ {nombre_campo} no puede estar vacío.")
        return False
    return True

def validar_nombre(nombre):
    if not validar_no_vacio(nombre, "Nombre"):
        return False

    if any(char.isdigit() for char in nombre):
        print("❌ El nombre no puede tener números.")
        return False

    partes = nombre.strip().split()
    if len(partes) < 2:
        print("❌ Debes ingresar nombre completo (Ej: Ana Pérez).")
        return False

    return True

def validar_email(email):
    if not validar_no_vacio(email, "Email"):
        return False

    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(patron, email):
        print("❌ Email inválido.")
        return False

    return True

def validar_telefono(telefono):
    if not validar_no_vacio(telefono, "Teléfono"):
        return False

    if not telefono.isdigit():
        print("❌ El teléfono debe tener solo números.")
        return False

    if len(telefono) < 8 or len(telefono) > 9:
        print("❌ Debe tener 8 o 9 dígitos.")
        return False

    return True

def validar_username(username):
    return validar_no_vacio(username, "Username")
