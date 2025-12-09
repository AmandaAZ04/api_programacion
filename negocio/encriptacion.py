import os
import hashlib
import binascii

class Encriptador:
    """
    Clase para encriptar y validar contraseñas
    usando PBKDF2-HMAC-SHA256.
    """

    @staticmethod
    def generar_salt():
        """Genera un salt aleatorio de 16 bytes en formato hexadecimal."""
        return binascii.hexlify(os.urandom(16)).decode()

    @staticmethod
    def encriptar(password: str, salt: str) -> str:
        """Devuelve el hash (string hex) de la contraseña usando el salt."""
        password_bytes = password.encode()
        salt_bytes = salt.encode()

        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',      # algoritmo
            password_bytes,
            salt_bytes,
            100000          # número de iteraciones
        )

        return binascii.hexlify(hash_bytes).decode()

    @staticmethod
    def comparar(password_ingresada: str, salt: str, hash_guardado: str) -> bool:
        """
        Compara la contraseña ingresada con el hash guardado.
        """
        hash_nuevo = Encriptador.encriptar(password_ingresada, salt)
        return hash_nuevo == hash_guardado