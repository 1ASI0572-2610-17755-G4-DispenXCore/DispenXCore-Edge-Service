from flask import Blueprint, request, jsonify
from iam.application.services import DeviceApplicationService

iam_api = Blueprint('iam_api', __name__)
application_service = DeviceApplicationService()

@iam_api.route('/api/v1/iam/devices/register', methods=['POST'])
def register_device():
    data = request.get_json() or {}
    device_id = data.get('device_id')
    mac_address = data.get('mac_address')
    ip_address = data.get('ip_address')

    if not device_id:
        return jsonify({"status": "error", "message": "device_id es requerido"}), 400

    # Si no se provee ip_address, podemos obtenerla de la request
    if not ip_address:
        ip_address = request.remote_addr

    resultado = application_service.registrar_dispositivo(device_id, mac_address, ip_address)
    
    if resultado["status"] == "error":
        return jsonify(resultado), 500
        
    return jsonify(resultado), 200

@iam_api.route('/api/v1/iam/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    resultado = application_service.obtener_dispositivo(device_id)
    if resultado["status"] == "error":
        return jsonify(resultado), 404
    return jsonify(resultado), 200
