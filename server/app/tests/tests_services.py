from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_services_id_permissions():
    response = client.get("/services/1")
    assert response.status_code == 403
    assert response.json() == {"detail": "Token missing."}


def test_get_services_id_actions_permissions():
    response = client.get("/services/1/actions")
    assert response.status_code == 403
    assert response.json() == {"detail": "Token missing."}


def test_get_services_id_reactions_permissions():
    response = client.get("/services/1/reactions")
    assert response.status_code == 403
    assert response.json() == {"detail": "Token missing."}
