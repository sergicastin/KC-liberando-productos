from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from prometheus_client import Counter, start_http_server
from kubernetes import client, config

app = FastAPI()

# Define the Prometheus counters
REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')
HEALTHCHECK_REQUESTS = Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Total number of requests to main endpoint')
BYE_ENDPOINT_REQUESTS = Counter('bye_requests_total', 'Total number of requests to say_bye endpoint')
POD_START_COUNT = Counter('pod_start_count', 'Total number of times the pod has started')

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

    @app.on_event("startup")
    async def startup_event():
        """Increment the pod start count when the application starts"""
        POD_START_COUNT.inc()

    @app.get("/health")
    async def health_check():
        """Implement health check endpoint"""
        REQUESTS.inc()
        HEALTHCHECK_REQUESTS.inc()
        return {"health": "ok"}

    @app.get("/")
    async def read_main():
        """Implement main endpoint"""
        REQUESTS.inc()
        MAIN_ENDPOINT_REQUESTS.inc()
        return {"msg": "Hello World"}
    
    @app.get("/bye")
    async def say_bye():
        """Implement bye endpoint"""
        BYE_ENDPOINT_REQUESTS.inc()
        return {"msg": "Bye Bye"}

def count_pods():
    """Count the number of pods with the specified name and namespace"""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    namespace = "fast-api"
    label_selector = "app=my-app-fast-api-webapp"
    pod_list = v1.list_namespaced_pod(namespace, label_selector=label_selector)
    return len(pod_list.items)

if __name__ == "__main__":
    # Expose the metrics endpoint
    start_http_server(8000)
    # Run the FastAPI server
    server = SimpleServer()
    import asyncio
    asyncio.run(server.run_server())
