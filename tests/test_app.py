from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "API online"


def test_error_endpoint_returns_500():
    response = client.get("/error")
    assert response.status_code == 500
    assert "erro" in response.json()
