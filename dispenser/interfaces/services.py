from flask import Blueprint, request, jsonify
from dispenser.application.services import DispensadorApplicationService

dispenser_api = Blueprint('dispenser_api', __name__)
application_service = DispensadorApplicationService()

@dispenser_api.route('/api/v1/dispenser/activate', methods=['POST'])
def activate_dispenser():
    data = request.get_json() or {}
    device_id = data.get('device_id')
    supply_type = data.get('supply_type')

    if not device_id:
        return jsonify({"status": "error", "message": "device_id es requerido"}), 400

    resultado = application_service.activar_dispensador_manualmente(device_id, supply_type)
    
    if resultado["status"] == "error":
        return jsonify(resultado), 500
        
    return jsonify(resultado), 200

@dispenser_api.route('/api/v1/dispenser/pending', methods=['GET'])
def get_pending():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"status": "error", "message": "device_id es requerido como query parameter"}), 400
        
    resultado = application_service.obtener_dispensacion_pendiente(device_id)
    return jsonify(resultado), 200

@dispenser_api.route('/api/v1/dispenser/confirm', methods=['POST'])
def confirm_dispense():
    data = request.get_json() or {}
    event_id = data.get('event_id')
    status = data.get('status', 'COMPLETED')

    if not event_id:
        return jsonify({"status": "error", "message": "event_id es requerido"}), 400

    resultado = application_service.confirmar_dispensacion(int(event_id), status)
    
    if resultado["status"] == "error":
        return jsonify(resultado), 404
        
    return jsonify(resultado), 200