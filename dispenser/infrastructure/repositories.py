from dispenser.domain.entities import DispenserEvent
from dispenser.infrastructure.models import DispenserEventORM

class DispenserRepository:
    def save(self, event: DispenserEvent) -> DispenserEvent:
        if event.id:
            orm = DispenserEventORM.get_by_id(event.id)
            orm.status = event.status
            orm.save()
        else:
            orm = DispenserEventORM.create(
                device_id=event.device_id,
                event_type=event.event_type,
                supply_type=event.supply_type,
                status=event.status,
                created_at=event.created_at
            )
            event.id = orm.id
        return event

    def find_pending_by_device_id(self, device_id: str) -> DispenserEvent:
        try:
            orm = DispenserEventORM.select().where(
                (DispenserEventORM.device_id == device_id) &
                (DispenserEventORM.status == 'PENDING')
            ).order_by(DispenserEventORM.created_at.asc()).first()
            
            if orm:
                return DispenserEvent(
                    id=orm.id,
                    device_id=orm.device_id,
                    event_type=orm.event_type,
                    supply_type=orm.supply_type,
                    status=orm.status,
                    created_at=orm.created_at
                )
        except DispenserEventORM.DoesNotExist:
            pass
        return None

    def find_by_id(self, event_id: int) -> DispenserEvent:
        try:
            orm = DispenserEventORM.get_by_id(event_id)
            return DispenserEvent(
                id=orm.id,
                device_id=orm.device_id,
                event_type=orm.event_type,
                supply_type=orm.supply_type,
                status=orm.status,
                created_at=orm.created_at
            )
        except DispenserEventORM.DoesNotExist:
            return None

    def update_status(self, event_id: int, status: str) -> bool:
        try:
            orm = DispenserEventORM.get_by_id(event_id)
            orm.status = status
            orm.save()
            return True
        except DispenserEventORM.DoesNotExist:
            return False
