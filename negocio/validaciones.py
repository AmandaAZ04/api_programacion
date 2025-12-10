import re

# VALIDAR QUE EL CAMPO NO ESTÉ VACÍO
def validar_no_vacio(valor, nombre_campo):
    if not valor.strip():
        print(f"El campo '{nombre_campo}' no puede estar vacío.")
        return False
    return True

# VALIDAR NOMBRE COMPLETO (mínimo 2 palabras, sin números)
def validar_nombre(nombre):
    if not validar_no_vacio(nombre, "Nombre"):
        return False

    if any(char.isdigit() for char in nombre):
        print("El nombre no puede contener números")
        return False

    partes = nombre.strip().split()

    if len(partes) < 2:
        print("Debe ingresar su nombre completo (Ej: Ana Perez)")
        return False

    return True

# VALIDAR EMAIL (formato correcto con regex)
def validar_email(email):
    if not validar_no_vacio(email, "Email"):
        return False

    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(patron, email):
        print("Email inválido. Debe tener formato ejemplo@dominio.com")
        return False

    return True

# VALIDAR TELÉFONO (solo números, 8–9 dígitos)
def validar_telefono(telefono):
    if not validar_no_vacio(telefono, "Teléfono"):
        return False

    if not telefono.isdigit():
        print("El teléfono debe contener solo números.")
        return False

    if len(telefono) > 9 or len(telefono) < 8:
        print("El teléfono debe tener 8 o 9 dígitos.")
        return False

    return True

# VALIDAR USERNAME (no vacío)
def validar_username(username):
    return validar_no_vacio(username, "Username")