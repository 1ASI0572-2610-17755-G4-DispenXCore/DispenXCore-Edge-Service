# Walkthrough de Implementación: DispenXCore Edge Service

Hemos completado el desarrollo de cada uno de los Bounded Contexts del Edge Service siguiendo el diseño de arquitectura limpia (Clean Architecture) y hemos verificado con éxito el flujo de control híbrido (push/pull) del servomotor.

---

## Cambios Realizados y Archivos Creados

### 1. Bounded Context: Shared
- [database.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/shared/infrastructure/database.py): Inicialización del ORM Peewee con SQLite local (`dispenx.db`).

### 2. Bounded Context: IAM
- [entities.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/iam/domain/entities.py): Entidad de dominio `Device`.
- [models.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/iam/infrastructure/models.py): Tabla `DeviceORM` para guardar la IP, MAC y estado del ESP32.
- [repositories.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/iam/infrastructure/repositories.py): Operaciones de consulta/guardado de dispositivos.
- [services.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/iam/application/services.py): Registro y obtención de dispositivos.
- [services.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/iam/interfaces/services.py): Rutas de registro `/api/v1/iam/devices/register` y consulta `/api/v1/iam/devices/<device_id>`.

### 3. Bounded Context: Inventory
- [entities.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/inventory/domain/entities.py): Entidad de dominio `SensorReading`.
- [models.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/inventory/infrastructure/models.py): Tabla `DatoSensorORM` para telemetría.
- [repositories.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/inventory/infrastructure/repositories.py): Persistencia de sensores y obtención de últimas lecturas consolidadas.
- [hardware_sensors.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/inventory/infrastructure/hardware_sensors.py): Cliente de peticiones salientes para leer del ESP32 directamente.
- [services.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/inventory/application/services.py): Casos de uso de telemetría completa y registro individual.
- [services.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/inventory/interfaces/services.py): Rutas de ingestión `/api/v1/inventory/telemetry`, consulta `/api/v1/inventory/latest` y trigger manual `/api/v1/inventory/trigger-read`.

### 4. Bounded Context: Dispenser
- [entities.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/dispenser/domain/entities.py): Entidad `DispenserEvent`.
- [models.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/dispenser/infrastructure/models.py): Añadido campo `status` a `DispenserEventORM`.
- [repositories.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/dispenser/infrastructure/repositories.py): Colas de eventos con estado `PENDING`, `COMPLETED`, `FAILED`.
- [hardware_motor.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/dispenser/infrastructure/hardware_motor.py): Controlador de red local con soporte para comandos POST (`/activate` y `/abrir_compuerta`).
- [services.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/dispenser/application/services.py): Encolamiento de eventos de dispensación y trigger en hilos secundarios (`threading.Thread`).
- [services.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/dispenser/interfaces/services.py): Rutas de activación `/api/v1/dispenser/activate`, obtención de pendientes `/api/v1/dispenser/pending` y confirmación `/api/v1/dispenser/confirm`.

### 5. Archivo Principal: App
- [app.py](file:///c:/Users/Ricardo/Downloads/dispenXcore-edge-service/app.py): Inicialización de Flask, registro de todos los Blueprints y creación automática de tablas.

---

## Verificación de Resultados

Hemos validado el servicio con un script de simulación de dispositivo IoT (`simulate_esp32.py` ubicado en la carpeta scratch).

El log de ejecución completa demostró el correcto funcionamiento del flujo híbrido (Push alternativo y Pull de respaldo):

```
--- 1. Probando conexion con el servicio Edge ---
Index response: {'name': 'DispenXCore Edge Service', 'status': 'online', 'version': '1.0.0'}

--- 2. Registrando dispositivo (IAM) ---
Register response: {'device': {'device_id': 'esp32_01', 'id': 1, 'ip_address': '127.0.0.1', 'last_seen': '2026-06-12T18:59:48.659732', 'mac_address': 'AA:BB:CC:DD:EE:FF'}, 'message': 'Dispositivo registrado/actualizado con éxito', 'status': 'success'}

--- 3. Enviando telemetria de sensores (Inventory) ---
Telemetry response: {'readings': [{'device_id': 'esp32_01', 'id': 5, 'sensor_type': 'level', 'timestamp': '2026-06-12T18:59:48.677168', 'value': 82.5}, {'device_id': 'esp32_01', 'id': 6, 'sensor_type': 'weight', 'timestamp': '2026-06-12T18:59:48.683513', 'value': 350.0}, {'device_id': 'esp32_01', 'id': 7, 'sensor_type': 'temperature', 'timestamp': '2026-06-12T18:59:48.686953', 'value': 22.8}, {'device_id': 'esp32_01', 'id': 8, 'sensor_type': 'humidity', 'timestamp': '2026-06-12T18:59:48.690875', 'value': 58.4}], 'status': 'success'}

--- 4. Consultando las ultimas lecturas ---
Latest telemetry: {'device_id': 'esp32_01', 'status': 'success', 'telemetry': {'humidity': 58.4, 'level': 82.5, 'temperature': 22.8, 'weight': 350.0}, 'timestamp': '2026-06-12T18:59:48.699272'}

--- 5. Simulando que la App Movil Flutter pide activar el dispensador ---
Activate response: {'event': {'created_at': '2026-06-12T18:59:48.701478', 'device_id': 'esp32_01', 'event_type': 'MANUAL_DISPENSE', 'id': 1, 'status': 'PENDING', 'supply_type': 'Legumbres'}, 'message': 'Dispensación encolada correctamente', 'status': 'success'}

--- 6. ESP32 haciendo Polling para ver si hay dispensacion pendiente ---
Pending polling response: {'dispense': True, 'event_id': 1, 'event_type': 'MANUAL_DISPENSE', 'supply_type': 'Legumbres'}

[ESP32 SIMULADO] ¡Orden de dispensacion recibida! Activando servomotor SG90 para dispensar Legumbres...

--- 7. ESP32 confirmando que se completo la dispensacion ---
Confirm response: {'message': 'Dispensación actualizada a COMPLETED', 'status': 'success'}

--- 8. Re-verificando si hay mas pendientes ---
Pending polling response (deberia ser false): {'dispense': False}
```

El servidor detectó la solicitud de la app Flutter, guardó el estado `PENDING` al no poder comunicarse directamente con la IP simulada localmente, y la dispensación se completó exitosamente cuando el simulador de ESP32 la obtuvo mediante **polling** y la confirmó.
