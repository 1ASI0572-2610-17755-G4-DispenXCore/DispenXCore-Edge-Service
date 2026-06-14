from flask import Blueprint, request, jsonify
from inventory.application.services import InventoryApplicationService

inventory_api = Blueprint('inventory_api', __name__)
application_service = InventoryApplicationService()

@inventory_api.route('/api/v1/inventory/telemetry', methods=['POST'])
def receive_telemetry():
    data = request.get_json() or {}
    device_id = data.get('device_id')
    readings = data.get('readings')  # Ej: {"level": 70, "weight": 200, "temperature": 23, "humidity": 55}

    if not device_id:
        return jsonify({"status": "error", "message": "device_id es requerido"}), 400
    if not readings or not isinstance(readings, dict):
        return jsonify({"status": "error", "message": "readings es requerido y debe ser un objeto"}), 400

    resultado = application_service.registrar_telemetria_completa(device_id, readings)
    return jsonify(resultado), 200

@inventory_api.route('/api/v1/inventory/latest', methods=['GET'])
def get_latest():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"status": "error", "message": "device_id es requerido como query parameter"}), 400

    resultado = application_service.obtener_telemetria_reciente(device_id)
    return jsonify(resultado), 200

@inventory_api.route('/api/v1/inventory/trigger-read', methods=['POST'])
def trigger_read():
    data = request.get_json() or {}
    device_id = data.get('device_id')
    if not device_id:
        return jsonify({"status": "error", "message": "device_id es requerido"}), 400

    resultado = application_service.solicitar_lectura_dispositivo(device_id)
    if resultado["status"] == "error":
        return jsonify(resultado), 500
    return jsonify(resultado), 200
