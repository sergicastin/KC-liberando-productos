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
    # Iniciar el servidor HTTP para exponer métricas de Prometheus
    start_http_server(8000)
    
    # Crear una instancia de Container
    container = Container()
    
    # Obtener el bucle de eventos de asyncio
    loop = asyncio.get_event_loop()
    
    # Asegurar que la función start_server se ejecute de forma asíncrona en el bucle de eventos
    asyncio.ensure_future(container.start_server(), loop=loop)
    
    # Ejecutar el bucle de eventos para mantener el programa en funcionamiento
    loop.run_forever()
