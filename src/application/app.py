from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from prometheus_client import Counter

# Define todas las métricas en el mismo archivo
REQUESTS = Counter('server_requests_total', 'Todos los request')
HEALTHCHECK_REQUESTS = Counter('healthcheck_requests_total', 'Todos los request a healthcheck')
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Todos los request al endpoint principal')
BYE_ENDPOINT_REQUESTS = Counter('bye_requests_total', 'Todos los request a say_bye endpoint')
POD_STARTUPS = Counter('TOTAL_POD_STARTUPS', 'Todas las veces que se ha arrancado la aplicación')

app = FastAPI()

class SimpleServer:
    """
    SimpleServer class define FastAPI configuration and implemented endpoints
    """

    _hypercorn_config = None

    def __init__(self):
        self._hypercorn_config = HyperCornConfig()

    async def run_server(self):
        """Starts the server with the config parameters"""
        self._hypercorn_config.bind = ['0.0.0.0:8081']
        self._hypercorn_config.keep_alive_timeout = 90
        await serve(app, self._hypercorn_config)

    @app.get("/health")
    async def health_check():
        """Implement health check endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the requests to healtcheck endpoint
        HEALTHCHECK_REQUESTS.inc()
        return {"health": "ok"}

    @app.get("/")
    async def read_main():
        """Implement main endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the total number of calls in the main endpoint
        MAIN_ENDPOINT_REQUESTS.inc()
        return {"msg": "Hello World"}
    
    @app.get("/bye")
    async def say_bye():
        """Implement bye endpoint"""
        REQUESTS.inc()
        # Incrementa el contador utilizado para registrar el número total de llamadas al servidor web
        BYE_ENDPOINT_REQUESTS.inc()
        return {"msg": "Bye Bye"}

    async def on_startup(self):
        """Function to run on startup"""
        # Incrementa el contador utilizado para registrar el inicio del pod
        POD_STARTUPS.inc()

# Instancia de la clase SimpleServer
simple_server = SimpleServer()

# Ejecución del servidor
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(simple_server.on_startup())
    loop.run_until_complete(simple_server.run_server())
    loop.close()
