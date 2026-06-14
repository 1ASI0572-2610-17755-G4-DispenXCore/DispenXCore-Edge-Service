from iam.domain.entities import Device
from iam.infrastructure.models import DeviceORM

class DeviceRepository:
    def save(self, device: Device) -> Device:
        device_orm, created = DeviceORM.get_or_create(
            device_id=device.device_id,
            defaults={
                "mac_address": device.mac_address,
                "ip_address": device.ip_address,
                "last_seen": device.last_seen
            }
        )
        if not created:
            device_orm.mac_address = device.mac_address
            device_orm.ip_address = device.ip_address
            device_orm.last_seen = device.last_seen
            device_orm.save()
        
        device.id = device_orm.id
        return device

    def find_by_device_id(self, device_id: str) -> Device:
        try:
            device_orm = DeviceORM.get(DeviceORM.device_id == device_id)
            return Device(
                id=device_orm.id,
                device_id=device_orm.device_id,
                mac_address=device_orm.mac_address,
                ip_address=device_orm.ip_address,
                last_seen=device_orm.last_seen
            )
        except DeviceORM.DoesNotExist:
            return None
