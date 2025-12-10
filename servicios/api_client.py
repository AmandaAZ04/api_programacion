# servicios/api_client.py

import requests

class APIClient:
    """
    Cliente HTTP para interactuar con APIs externas.
    Maneja GET, POST, PUT y DELETE con manejo básico de errores.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    # ======================
    # GET
    # ======================
    def get(self, endpoint):
        try:
            resp = requests.get(self.base_url + endpoint, timeout=5)

            if resp.status_code == 200:
                return {"ok": True, "status": 200, "data": resp.json()}

            elif resp.status_code == 404:
                return {"ok": False, "status": 404, "error": "Recurso no encontrado"}

            elif resp.status_code == 400:
                return {"ok": False, "status": 400, "error": "Solicitud incorrecta"}

            return {
                "ok": False,
                "status": resp.status_code,
                "error": "Error inesperado del servidor"
            }

        except requests.exceptions.RequestException:
            return {"ok": False, "status": 0, "error": "Error de conexión con la API"}

    # ======================
    # POST
    # ======================
    def post(self, endpoint, data):
        try:
            resp = requests.post(self.base_url + endpoint, json=data, timeout=5)

            if resp.status_code in (200, 201):
                return {"ok": True, "status": resp.status_code, "data": resp.json()}

            elif resp.status_code == 400:
                return {"ok": False, "status": 400, "error": "Datos inválidos"}

            return {"ok": False, "status": resp.status_code, "error": "Error inesperado"}

        except requests.exceptions.RequestException:
            return {"ok": False, "status": 0, "error": "Error de red"}

    # ======================
    # PUT
    # ======================
    def put(self, endpoint, data):
        try:
            resp = requests.put(self.base_url + endpoint, json=data, timeout=5)

            if resp.status_code == 200:
                return {"ok": True, "status": 200, "data": resp.json()}

            elif resp.status_code == 404:
                return {"ok": False, "status": 404, "error": "Recurso no encontrado"}

            return {"ok": False, "status": resp.status_code, "error": "Error desconocido"}

        except requests.exceptions.RequestException:
            return {"ok": False, "status": 0, "error": "No hay conexión"}

    # ======================
    # DELETE
    # ======================
    def delete(self, endpoint):
        try:
            resp = requests.delete(self.base_url + endpoint, timeout=5)

            if resp.status_code in (200, 204):
                return {"ok": True, "status": resp.status_code}

            if resp.status_code == 404:
                return {"ok": False, "status": 404, "error": "No encontrado"}

            return {"ok": False, "status": resp.status_code, "error": "Error inesperado"}

        except requests.exceptions.RequestException:
            return {"ok": False, "status": 0, "error": "Error de red"}
