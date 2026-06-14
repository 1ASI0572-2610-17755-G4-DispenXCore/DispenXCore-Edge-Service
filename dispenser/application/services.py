import threading
from datetime import datetime
from dispenser.domain.entities import DispenserEvent
from dispenser.infrastructure.repositories import DispenserRepository
from dispenser.infrastructure.hardware_motor import ESP32MotorClient
from iam.infrastructure.repositories import DeviceRepository

class DispensadorApplicationService:
    def __init__(self):
        self.dispenser_repository = DispenserRepository()
        self.device_repository = DeviceRepository()
        self.motor_client = ESP32MotorClient()

    def activar_dispensador_manualmente(self, device_id: str, supply_type: str) -> dict:
        event = DispenserEvent(
            device_id=device_id,
            event_type='MANUAL_DISPENSE',
            supply_type=supply_type or 'General',
            status='PENDING',
            created_at=datetime.now()
        )
        saved_event = self.dispenser_repository.save(event)

        # Lanza hilo para intentar la activación directa (Push)
        thread = threading.Thread(
            target=self._intentar_notificacion_directa,
            args=(saved_event.id, device_id, supply_type)
        )
        thread.daemon = True
        thread.start()

        return {
            "status": "success",
            "message": "Dispensación encolada correctamente",
            "event": saved_event.to_dict()
        }

    def _intentar_notificacion_directa(self, event_id: int, device_id: str, supply_type: str):
        device = self.device_repository.find_by_device_id(device_id)
        if not device or not device.ip_address:
            return  # No hay IP registrada, dependerá del Polling (Pull)

        # Intenta disparar directamente por HTTP al ESP32
        success = self.motor_client.trigger_dispense(device.ip_address, supply_type)
        if success:
            # Si el ESP32 respondió con éxito, marcamos como COMPLETED
            self.dispenser_repository.update_status(event_id, 'COMPLETED')

    def obtener_dispensacion_pendiente(self, device_id: str) -> dict:
        event = self.dispenser_repository.find_pending_by_device_id(device_id)
        if event:
            return {
                "dispense": True,
                "event_id": event.id,
                "event_type": event.event_type,
                "supply_type": event.supply_type
            }
        return {"dispense": False}

    def confirmar_dispensacion(self, event_id: int, status: str) -> dict:
        actualizado = self.dispenser_repository.update_status(event_id, status)
        if actualizado:
            return {"status": "success", "message": f"Dispensación actualizada a {status}"}
        return {"status": "error", "message": "No se encontró el evento de dispensación"}
