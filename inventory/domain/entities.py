from datetime import datetime

class SensorReading:
    def __init__(self, device_id: str, sensor_type: str, value: float, timestamp: datetime = None, id: int = None):
        self.id = id
        self.device_id = device_id
        self.sensor_type = sensor_type  # 'level', 'weight', 'temperature', 'humidity'
        self.value = value
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "sensor_type": self.sensor_type,
            "value": self.value,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
