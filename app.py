from flask import Flask
from shared.infrastructure.database import db
from iam.infrastructure.models import DeviceORM
from inventory.infrastructure.models import DatoSensorORM
from dispenser.infrastructure.models import DispenserEventORM

from iam.interfaces.services import iam_api
from inventory.interfaces.services import inventory_api
from dispenser.interfaces.services import dispenser_api

app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(iam_api)
app.register_blueprint(inventory_api)
app.register_blueprint(dispenser_api)

# Crear tablas e inicializar BD al arrancar
def init_db():
    db.connect()
    db.create_tables([DeviceORM, DatoSensorORM, DispenserEventORM])
    db.close()

init_db()

@app.route('/')
def index():
    return {
        "name": "DispenXCore Edge Service",
        "version": "1.0.0",
        "status": "online"
    }

if __name__ == '__main__':
    # Ejecutar en host 0.0.0.0 para permitir el acceso del ESP32 en la red local
    app.run(host='0.0.0.0', port=5000, debug=True)