from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_areas_permissions():
    response = client.get("/areas")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}

def test_get_areas_id_permissions():
    response = client.get("/areas/1")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}

def test_post_areas_permissions():
    response = client.post("/areas")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}
    
def test_delete_areas_permissions():
    response = client.delete("/areas/1")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}
