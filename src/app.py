import asyncio
from prometheus_client import start_http_server
from application.app import SimpleServer

class Container:
    """
    Class Container configure necessary methods for launch application
    """

    def __init__(self):
        self._simple_server = SimpleServer()

    async def start_server(self):
        """Function for start server"""
        await self._simple_server.run_server()

if __name__ == "__main__":
    # Iniciar un servidor HTTP para exponer métricas Prometheus en el puerto 8000
    start_http_server(8000)
    
    # Instanciar la clase Container
    container = Container()
    
    # Obtener el bucle de eventos asyncio
    loop = asyncio.get_event_loop()
    
    # Iniciar el servidor FastAPI en el bucle de eventos asyncio
    asyncio.ensure_future(container.start_server(), loop=loop)
    
    # Ejecutar el bucle de eventos asyncio
    loop.run_forever()
