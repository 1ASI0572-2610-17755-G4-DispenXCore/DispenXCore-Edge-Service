from datetime import datetime

class DispenserEvent:
    def __init__(self, device_id: str, event_type: str, supply_type: str, status: str = 'PENDING', created_at: datetime = None, id: int = None):
        self.id = id
        self.device_id = device_id
        self.event_type = event_type  # MANUAL_DISPENSE, SCHEDULED_DISPENSE
        self.supply_type = supply_type  # Arroz, Azúcar, Legumbres
        self.status = status  # PENDING, COMPLETED, FAILED
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "event_type": self.event_type,
            "supply_type": self.supply_type,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
