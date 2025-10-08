from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users_me_permissions():
    response = client.get("/users/me")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}

def test_delete_users_me_permissions():
    response = client.delete("/users/me")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}

def test_get_users_permissions():
    response = client.get("/users")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}

def test_get_users_id_permissions():
    response = client.get("/users/1")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}

def test_delete_users_id_permissions():
    response = client.delete("/users/1")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}
