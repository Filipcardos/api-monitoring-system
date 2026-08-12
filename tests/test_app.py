<<<<<<< HEAD
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
=======
import importlib

from fastapi.testclient import TestClient


def _fresh_client(monkeypatch, tmp_path, cron_secret=""):
    """Cria um client com um repositório isolado (arquivo JSON temporário)."""
    monkeypatch.setenv("CRON_SECRET", cron_secret)
    monkeypatch.setenv("MONITOR_URL", "http://127.0.0.1:8000")

    import config
    import monitor
    import app as app_module
    from repository import monitoring_repository as repo

    importlib.reload(config)
    monkeypatch.setattr(repo, "_LOCAL_FILE", tmp_path / "history.json")
    monkeypatch.setattr(repo, "_USE_UPSTASH", False)
    importlib.reload(monitor)
    importlib.reload(app_module)

    return TestClient(app_module.app), app_module


def test_health():
    from app import app

    client = TestClient(app)
>>>>>>> master
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


<<<<<<< HEAD
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "API online"


def test_error_endpoint_returns_500():
    response = client.get("/error")
    assert response.status_code == 500
    assert "erro" in response.json()
=======
def test_error_endpoint_returns_500():
    from app import app

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 500
    assert "erro" in response.json()


def test_summary_without_data(monkeypatch, tmp_path):
    client, _ = _fresh_client(monkeypatch, tmp_path)
    response = client.get("/api/monitoring/summary")
    assert response.status_code == 200
    assert response.json()["has_data"] is False


def test_cron_requires_secret_when_configured(monkeypatch, tmp_path):
    client, _ = _fresh_client(monkeypatch, tmp_path, cron_secret="topsecret")
    unauthorized = client.get("/api/cron/monitor")
    assert unauthorized.status_code == 401

    authorized = client.get(
        "/api/cron/monitor", headers={"Authorization": "Bearer topsecret"}
    )
    assert authorized.status_code == 200
    assert authorized.json()["status"] == "ok"
>>>>>>> master
