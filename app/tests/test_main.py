from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Secure CI/CD demo application is running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_items_endpoint():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1