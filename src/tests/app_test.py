from fastapi.testclient import TestClient
import pytest

from ..app import app  # Ajusta la importación al nuevo lugar de tu app

client = TestClient(app)

class TestSimpleServer:
    """
    TestSimpleServer class for testing SimpleServer
    """
    @pytest.mark.asyncio
    async def test_read_health(self):  # Ajusta el nombre del método de prueba
        """Tests the health check endpoint"""
        response = client.get("/health")  # Añade "/" al inicio del endpoint

        assert response.status_code == 200
        assert response.json() == {"health": "ok"}

    @pytest.mark.asyncio
    async def test_read_main(self):  # Ajusta el nombre del método de prueba
        """Tests the main endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    @pytest.mark.asyncio
    async def test_read_bye(self):  # Ajusta el nombre del método de prueba
        """Tests the bye endpoint"""
        response = client.get("/bye")

        assert response.status_code == 200
        assert response.json() == {"msg": "Bye Bye"}
