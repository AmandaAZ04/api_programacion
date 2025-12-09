import requests

class APIClient:
    """
    Cliente para hacer solicitudes HTTP a la API jsonplaceholder.
    Maneja GET, POST, PUT y DELETE con control de errores.
    """

    def __init__(self, base_url):
        self.base = base_url.rstrip('/')

    # ---------------------------
    # GET
    # ---------------------------
    def get(self, path):
        url = f"{self.base}/{path.lstrip('/')}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            print("❌ Error HTTP (GET):", e)
        except Exception as e:
            print("❌ Error inesperado (GET):", e)
        return None

    # ---------------------------
    # POST
    # ---------------------------
    def post(self, path, data):
        url = f"{self.base}/{path.lstrip('/')}"
        try:
            resp = requests.post(url, json=data, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            print("❌ Error HTTP (POST):", e)
        except Exception as e:
            print("❌ Error inesperado (POST):", e)
        return None

    # ---------------------------
    # PUT
    # ---------------------------
    def put(self, path, data):
        url = f"{self.base}/{path.lstrip('/')}"
        try:
            resp = requests.put(url, json=data, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            print("❌ Error HTTP (PUT):", e)
        except Exception as e:
            print("❌ Error inesperado (PUT):", e)
        return None

    # ---------------------------
    # DELETE
    # ---------------------------
    def delete(self, path):
        url = f"{self.base}/{path.lstrip('/')}"
        try:
            resp = requests.delete(url, timeout=10)
            resp.raise_for_status()
            return resp.status_code
        except requests.HTTPError as e:
            print("❌ Error HTTP (DELETE):", e)
        except Exception as e:
            print("❌ Error inesperado (DELETE):", e)
        return None
