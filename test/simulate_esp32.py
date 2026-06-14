import time
import requests
import sys

BASE_URL = "http://127.0.0.1:5000"
DEVICE_ID = "esp32_02"

def test_api():
    print("--- 1. Probando conexion con el servicio Edge ---")
    try:
        res = requests.get(f"{BASE_URL}/")
        print(f"Index response: {res.json()}")
    except Exception as e:
        print(f"Error conectando al servidor Flask: {e}")
        print("Asegurate de que 'python app.py' este corriendo en http://127.0.0.1:5000")
        sys.exit(1)

    print("\n--- 2. Registrando dispositivo (IAM) ---")
    reg_data = {
        "device_id": DEVICE_ID,
        "mac_address": "AA:BB:CC:DD:EE:FG",
        "ip_address": "127.0.0.2"
    }
    res = requests.post(f"{BASE_URL}/api/v1/iam/devices/register", json=reg_data)
    print(f"Register response: {res.json()}")

    print("\n--- 3. Enviando telemetria de sensores (Inventory) ---")
    telemetry_data = {
        "device_id": DEVICE_ID,
        "readings": {
            "level": 90.5,
            "weight": 450.0,
            "temperature": 50.8,
            "humidity": 20.4
        }
    }
    res = requests.post(f"{BASE_URL}/api/v1/inventory/telemetry", json=telemetry_data)
    print(f"Telemetry response: {res.json()}")

    print("\n--- 4. Consultando las ultimas lecturas ---")
    res = requests.get(f"{BASE_URL}/api/v1/inventory/latest?device_id={DEVICE_ID}")
    print(f"Latest telemetry: {res.json()}")

    print("\n--- 5. Simulando que la App Movil Flutter pide activar el dispensador ---")
    activate_payload = {
        "device_id": DEVICE_ID,
        "supply_type": "Legumbres"
    }
    res = requests.post(f"{BASE_URL}/api/v1/dispenser/activate", json=activate_payload)
    activate_res = res.json()
    print(f"Activate response: {activate_res}")

    print("\n--- 6. ESP32 haciendo Polling para ver si hay dispensacion pendiente ---")
    res = requests.get(f"{BASE_URL}/api/v1/dispenser/pending?device_id={DEVICE_ID}")
    pending_res = res.json()
    print(f"Pending polling response: {pending_res}")

    if pending_res.get("dispense"):
        event_id = pending_res["event_id"]
        supply = pending_res["supply_type"]
        print(f"\n[ESP32 SIMULADO] ¡Orden de dispensacion recibida! Activando servomotor SG90 para dispensar {supply}...")
        time.sleep(1)
        
        print("\n--- 7. ESP32 confirmando que se completo la dispensacion ---")
        confirm_payload = {
            "event_id": event_id,
            "status": "COMPLETED"
        }
        res = requests.post(f"{BASE_URL}/api/v1/dispenser/confirm", json=confirm_payload)
        print(f"Confirm response: {res.json()}")

        print("\n--- 8. Re-verificando si hay mas pendientes ---")
        res = requests.get(f"{BASE_URL}/api/v1/dispenser/pending?device_id={DEVICE_ID}")
        print(f"Pending polling response (deberia ser false): {res.json()}")

if __name__ == '__main__':
    test_api()

