import threading
from datetime import datetime
from inventory.domain.entities import SensorReading
from inventory.infrastructure.repositories import SensorRepository
from inventory.infrastructure.hardware_sensors import ESP32SensorClient
from iam.infrastructure.repositories import DeviceRepository
from shared.infrastructure.backend_client import BackendClient

class InventoryApplicationService:
    def __init__(self):
        self.sensor_repository = SensorRepository()
        self.device_repository = DeviceRepository()
        self.sensor_client = ESP32SensorClient()
        self.backend_client = BackendClient()

    def registrar_lectura(self, device_id: str, sensor_type: str, value: float) -> dict:
        reading = SensorReading(
            device_id=device_id,
            sensor_type=sensor_type,
            value=value,
            timestamp=datetime.now()
        )
        saved = self.sensor_repository.save(reading)
        return {"status": "success", "reading": saved.to_dict()}

    def registrar_telemetria_completa(self, device_id: str, readings: dict) -> dict:
        saved_readings = []
        for s_type, value in readings.items():
            if s_type in ['level', 'weight', 'temperature', 'humidity'] and value is not None:
                reading = SensorReading(
                    device_id=device_id,
                    sensor_type=s_type,
                    value=float(value),
                    timestamp=datetime.now()
                )
                self.sensor_repository.save(reading)
                saved_readings.append(reading.to_dict())

        # Enviar al backend de forma asíncrona
        thread = threading.Thread(
            target=self.backend_client.enviar_telemetria,
            args=(device_id, readings)
        )
        thread.daemon = True
        thread.start()

        return {"status": "success", "readings": saved_readings}

    def obtener_telemetria_reciente(self, device_id: str) -> dict:
        readings = self.sensor_repository.get_latest_readings(device_id)
        return {
            "status": "success",
            "device_id": device_id,
            "telemetry": {r.sensor_type: r.value for r in readings},
            "timestamp": datetime.now().isoformat()
        }

    def solicitar_lectura_dispositivo(self, device_id: str) -> dict:
        device = self.device_repository.find_by_device_id(device_id)
        if not device or not device.ip_address:
            return {"status": "error", "message": "Dispositivo o IP no registrada"}
        
        data = self.sensor_client.fetch_sensors(device.ip_address)
        if not data:
            return {"status": "error", "message": "No se pudo conectar con el dispositivo ESP32"}
        
        return self.registrar_telemetria_completa(device_id, data)
