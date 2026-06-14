from datetime import datetime

class Device:
    def __init__(self, device_id: str, mac_address: str, ip_address: str, last_seen: datetime = None, id: int = None):
        self.id = id
        self.device_id = device_id
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.last_seen = last_seen or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }
