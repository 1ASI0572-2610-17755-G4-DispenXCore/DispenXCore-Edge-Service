import requests
import logging

class ESP32SensorClient:
    def fetch_sensors(self, ip_address: str) -> dict:
        """
        Hace un GET request al ESP32 para obtener la lectura de los sensores.
        Ejemplo de respuesta esperada:
        {
          "level": 75.5,
          "weight": 250.0,
          "temperature": 24.5,
          "humidity": 60.2
        }
        """
        try:
            url = f"http://{ip_address}/sensors"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json() or {}
            else:
                logging.error(f"ESP32 respondió con código {response.status_code}")
        except Exception as e:
            logging.error(f"Error consultando sensores en ESP32 ({ip_address}): {e}")
        return {}
