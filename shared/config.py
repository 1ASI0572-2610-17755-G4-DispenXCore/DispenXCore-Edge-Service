import os

# Configuración del Backend externo
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080/api/v1")
