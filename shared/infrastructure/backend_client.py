import requests
import logging
from shared.config import BACKEND_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackendClient:
    def __init__(self):
        self.base_url = BACKEND_URL

    def registrar_dispositivo(self, device_id: str, mac_address: str, ip_address: str) -> bool:
        """
        Publica el registro del dispositivo en el backend.
        Endpoint: POST /api/v1/devices
        """
        url = f"{self.base_url}/devices"
        payload = {
            "device_id": device_id,
            "mac_address": mac_address,
            "ip_address": ip_address
        }
        try:
            logger.info(f"[BACKEND-CLIENT] Enviando registro de dispositivo a {url}...")
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code in [200, 201]:
                logger.info(f"[BACKEND-CLIENT] Registro completado con éxito en el backend (Status: {response.status_code}).")
                return True
            else:
                logger.warning(f"[BACKEND-CLIENT] Backend respondió con código {response.status_code} al registrar dispositivo.")
        except Exception as e:
            logger.error(f"[BACKEND-CLIENT] Error conectando con el backend para registrar dispositivo: {e}")
        return False

    def enviar_telemetria(self, device_id: str, readings: dict) -> bool:
        """
        Publica las lecturas de los sensores al backend.
        Endpoint: POST /api/v1/telemetry
        """
        url = f"{self.base_url}/telemetry"
        payload = {
            "device_id": device_id,
            "readings": readings
        }
        try:
            logger.info(f"[BACKEND-CLIENT] Enviando telemetría a {url}...")
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code in [200, 201]:
                logger.info(f"[BACKEND-CLIENT] Telemetría enviada con éxito al backend (Status: {response.status_code}).")
                return True
            else:
                logger.warning(f"[BACKEND-CLIENT] Backend respondió con código {response.status_code} al enviar telemetría.")
        except Exception as e:
            logger.error(f"[BACKEND-CLIENT] Error conectando con el backend para enviar telemetría: {e}")
        return False

    def enviar_evento_dispensacion(self, device_id: str, event_id: int, event_type: str, supply_type: str, status: str) -> bool:
        """
        Publica la creación o actualización de un evento de dispensación en el backend.
        Endpoint: POST /api/v1/dispenser/events
        """
        url = f"{self.base_url}/dispenser/events"
        payload = {
            "device_id": device_id,
            "event_id": event_id,
            "event_type": event_type,
            "supply_type": supply_type,
            "status": status
        }
        try:
            logger.info(f"[BACKEND-CLIENT] Enviando evento de dispensación ({status}) a {url}...")
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code in [200, 201]:
                logger.info(f"[BACKEND-CLIENT] Evento de dispensación enviado con éxito al backend (Status: {response.status_code}).")
                return True
            else:
                logger.warning(f"[BACKEND-CLIENT] Backend respondió con código {response.status_code} al enviar evento de dispensación.")
        except Exception as e:
            logger.error(f"[BACKEND-CLIENT] Error conectando con el backend para enviar evento de dispensación: {e}")
        return False
