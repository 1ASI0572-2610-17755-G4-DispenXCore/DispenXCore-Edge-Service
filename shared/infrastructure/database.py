from peewee import SqliteDatabase

# Base de datos SQLite local unificada
db = SqliteDatabase('dispenx.db')

def init_db() -> None:
    db.connect()
    # Deferred imports para evitar referencias circulares
    from iam.infrastructure.models import DeviceORM
    from inventario.infrastructure.models import DatoSensorORM
    from dispensadores.infrastructure.models import DispenserEventORM
    
    db.create_tables([DeviceORM, DatoSensorORM, DispenserEventORM], safe=True)
    db.close()