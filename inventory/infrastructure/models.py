from peewee import Model, CharField, DateTimeField, FloatField, AutoField
from shared.infrastructure.database import db

class DatoSensorORM(Model):
    id = AutoField()
    device_id = CharField()
    sensor_type = CharField()  # level, weight, temperature, humidity
    value = FloatField()
    timestamp = DateTimeField()

    class Meta:
        database = db
        table_name = 'sensor_data'
