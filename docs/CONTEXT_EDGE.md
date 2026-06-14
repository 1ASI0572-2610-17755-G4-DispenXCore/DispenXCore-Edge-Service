# Contexto de Arquitectura Edge - DispenXCore

## 1. Stack de Hardware Conectado (IoT)
- Microcontrolador: ESP32 (Conexión vía Red Local WiFi).
- Sensores: Ultrasónico HC-SR04 (Nivel), Celda de Carga HX711 (Peso), DHT22 (Temperatura/Humedad).
- Actuadores: Servomotor SG90 (Apertura de compuerta).

## 2. Arquitectura de Software del Edge
- Framework: Flask (Python) con ORM Peewee sobre SQLite (dispenx.db).
- Estructura: Clean Architecture dividida por Bounded Contexts (DDD):
  - `iam/`: Identificación del dispositivo.
  - `inventory/`: Telemetría de sensores, validación local y persistencia (DatoSensorORM).
  - `dispenser/`: Control de actuadores físicos mediante hilos paralelos y endpoints HTTP locales para la App móvil Flutter (/api/v1/dispenser/activar).

## 3. Consideraciones Críticas de Control
- El Edge se ejecuta en una máquina local separada en la misma red que el hardware IoT.
- El control del Servomotor SG90 y la lectura de sensores se realiza mediante peticiones inalámbricas HTTP (requests de Python) hacia la IP local del ESP32.
- Las activaciones de hardware deben dispararse en hilos secundarios (`threading.Thread`) para evitar bloquear el bucle de eventos de Flask.