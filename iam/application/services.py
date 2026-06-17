import threading
from datetime import datetime
from iam.domain.entities import Device
from iam.infrastructure.repositories import DeviceRepository
from shared.infrastructure.backend_client import BackendClient

class DeviceApplicationService:
    def __init__(self):
        self.repository = DeviceRepository()
        self.backend_client = BackendClient()

    def registrar_dispositivo(self, device_id: str, mac_address: str, ip_address: str) -> dict:
        device = Device(
            device_id=device_id,
            mac_address=mac_address,
            ip_address=ip_address,
            last_seen=datetime.now()
        )
        saved_device = self.repository.save(device)

        # Enviar al backend de forma asíncrona
        thread = threading.Thread(
            target=self.backend_client.registrar_dispositivo,
            args=(device_id, mac_address, ip_address)
        )
        thread.daemon = True
        thread.start()

        return {
            "status": "success",
            "message": "Dispositivo registrado/actualizado con éxito",
            "device": saved_device.to_dict()
        }

    def obtener_dispositivo(self, device_id: str) -> dict:
        device = self.repository.find_by_device_id(device_id)
        if not device:
            return {"status": "error", "message": "Dispositivo no encontrado"}
        return {"status": "success", "device": device.to_dict()}
