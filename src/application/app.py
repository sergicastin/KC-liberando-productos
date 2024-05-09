from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from prometheus_client import Counter, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Definir contadores de métricas
REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')
HEALTHCHECK_REQUESTS = Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Total number of requests to main endpoint')
BYE_ENDPOINT_REQUESTS = Counter('bye_requests_total', 'Total number of requests to say_bye endpoint')

# Instanciar la clase Instrumentator para la instrumentación de Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Definir el endpoint /health
@app.get("/health")
async def health_check():
    """Implement health check endpoint"""
    # Incrementar el contador utilizado para registrar el número total de llamadas al servidor web
    REQUESTS.inc()
    # Incrementar el contador utilizado para registrar las solicitudes al punto final de verificación de salud
    HEALTHCHECK_REQUESTS.inc()
    return {"health": "ok"}

# Definir el endpoint /
@app.get("/")
async def read_main():
    """Implement main endpoint"""
    # Incrementar el contador utilizado para registrar el número total de llamadas al servidor web
    REQUESTS.inc()
    # Incrementar el contador utilizado para registrar el número total de llamadas en el punto final principal
    MAIN_ENDPOINT_REQUESTS.inc()
    return {"msg": "Hello World"}

# Definir el endpoint /bye
@app.get("/bye")
async def say_bye():
    """Implement bye endpoint"""
    # Incrementar el contador utilizado para registrar el número total de llamadas al servidor web
    BYE_ENDPOINT_REQUESTS.inc()
    return {"msg": "Bye Bye"}

# Definir el endpoint /metrics
@app.get("/metrics")
async def metrics():
    """Implement metrics endpoint"""
    # Generar las últimas métricas registradas en formato Prometheus
    return generate_latest()
