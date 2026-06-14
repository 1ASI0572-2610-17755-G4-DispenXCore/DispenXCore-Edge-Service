from inventory.domain.entities import SensorReading
from inventory.infrastructure.models import DatoSensorORM

class SensorRepository:
    def save(self, reading: SensorReading) -> SensorReading:
        orm = DatoSensorORM.create(
            device_id=reading.device_id,
            sensor_type=reading.sensor_type,
            value=reading.value,
            timestamp=reading.timestamp
        )
        reading.id = orm.id
        return reading

    def get_latest_readings(self, device_id: str) -> list:
        readings = []
        sensor_types = ['level', 'weight', 'temperature', 'humidity']
        for s_type in sensor_types:
            try:
                orm = DatoSensorORM.select().where(
                    (DatoSensorORM.device_id == device_id) & 
                    (DatoSensorORM.sensor_type == s_type)
                ).order_by(DatoSensorORM.timestamp.desc()).get()
                readings.append(SensorReading(
                    id=orm.id,
                    device_id=orm.device_id,
                    sensor_type=orm.sensor_type,
                    value=orm.value,
                    timestamp=orm.timestamp
                ))
            except DatoSensorORM.DoesNotExist:
                pass
        return readings
