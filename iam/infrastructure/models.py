from peewee import Model, CharField, DateTimeField, AutoField
from shared.infrastructure.database import db

class DeviceORM(Model):
    id = AutoField()
    device_id = CharField(unique=True)
    mac_address = CharField(null=True)
    ip_address = CharField(null=True)
    last_seen = DateTimeField()

    class Meta:
        database = db
        table_name = 'devices'
