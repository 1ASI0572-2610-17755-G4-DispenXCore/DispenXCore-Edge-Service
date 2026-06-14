import requests
import logging

class ServomotorNetworkController:
    """Envía la orden de activación al servomotor a través de la red local."""
    
    def __init__(self, esp32_ip: str = "192.168.1.50"):
        self.esp32_url = f"http://{esp32_ip}/abrir_compuerta"
        logging.basicConfig(level=logging.INFO)

    def rotar_para_abrir(self, segundos_abierto: float = 3.0) -> bool:
        try:
            logging.info(f"[EDGE-RED] Enviando comando de apertura inalámbrico al ESP32...")
            # Envia la orden por la red local
            response = requests.post(self.esp32_url, json={"duration": segundos_abierto}, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"[EDGE-RED] No se pudo comunicar con el hardware en red: {str(e)}")
            return False

class ESP32MotorClient:
    def trigger_dispense(self, ip_address: str, supply_type: str) -> bool:
        """
        Envía una petición POST al microcontrolador ESP32 para activar el servomotor SG90.
        Petición: POST http://<esp32-ip>/activate
        Body: {"supply_type": "Arroz"}
        """
        try:
            url = f"http://{ip_address}/activate"
            payload = {"supply_type": supply_type}
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                logging.info(f"ESP32 SG90 activado con éxito para: {supply_type}")
                return True
            else:
                # Intenta también el endpoint alternativo /abrir_compuerta
                url_alt = f"http://{ip_address}/abrir_compuerta"
                response_alt = requests.post(url_alt, json={"duration": 3.0, "supply_type": supply_type}, timeout=5)
                if response_alt.status_code == 200:
                    logging.info(f"ESP32 SG90 activado con éxito mediante endpoint alternativo para: {supply_type}")
                    return True
                logging.error(f"ESP32 respondió con código {response.status_code} al activar el servomotor SG90.")
        except Exception as e:
            logging.error(f"Error conectando con ESP32 en {ip_address} para activar motor: {e}")
        return False