from peewee import Model, CharField, DateTimeField, AutoField
from shared.infrastructure.database import db

class DispenserEventORM(Model):
    id = AutoField()
    device_id = CharField()
    event_type = CharField()      # MANUAL_DISPENSE, SCHEDULED_DISPENSE
    supply_type = CharField()     # Arroz, Azúcar, Legumbres
    status = CharField(default='PENDING') # PENDING, COMPLETED, FAILED
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'dispenser_events'