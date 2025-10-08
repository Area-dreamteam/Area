from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_reactions_id_permissions():
    response = client.get("/reactions/1")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Token missing.'}
