# negocio/encriptacion.py

import os
import hashlib
import binascii

class Encriptador:
    """Encriptación PBKDF2-HMAC-SHA256 para contraseñas."""

    @staticmethod
    def generar_salt():
        return binascii.hexlify(os.urandom(16)).decode()

    @staticmethod
    def encriptar(password: str, salt: str) -> str:
        password_bytes = password.encode()
        salt_bytes = salt.encode()

        hash_bytes = hashlib.pbkdf2_hmac(
            "sha256",
            password_bytes,
            salt_bytes,
            100000
        )

        return binascii.hexlify(hash_bytes).decode()

    @staticmethod
    def comparar(password_ingresada: str, salt: str, hash_guardado: str) -> bool:
        hash_nuevo = Encriptador.encriptar(password_ingresada, salt)
        return hash_nuevo == hash_guardado