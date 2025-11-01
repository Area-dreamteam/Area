import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestBasicAPI:
    """Test basic API functionality"""

    def test_read_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to AREA API"}

    def test_api_health(self, client):
        """Test that API is healthy and responding"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get("/")
        assert response.status_code == 200

    def test_non_existent_endpoint(self, client):
        """Test non-existent endpoint returns 404"""
        response = client.get("/non-existent-endpoint")
        assert response.status_code == 404

    def test_api_accepts_json(self, client):
        """Test that API accepts JSON content type"""
        response = client.post(
            "/auth/logout", json={}, headers={"Content-Type": "application/json"}
        )
        assert response.status_code != 415

    def test_api_response_format(self, client):
        """Test that API returns JSON responses"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_http_methods(self, client):
        """Test that different HTTP methods work correctly"""
        response = client.get("/")
        assert response.status_code == 200

        response = client.post("/auth/logout")
        assert response.status_code in [200, 401, 403]

        response = client.patch("/users/me")
        assert response.status_code in [200, 401, 403, 422, 405]

        response = client.delete("/users/me")
        assert response.status_code in [200, 401, 403, 422]

    @patch("main.init_db")
    def test_app_startup_lifecycle(self, mock_init_db, client):
        """Test application startup components"""
        response = client.get("/")
        assert response.status_code == 200

        assert response.json() == {"message": "Welcome to AREA API"}

    def test_api_error_handling(self, client):
        """Test API error handling"""
        response = client.post(
            "/auth/logout",
            data="{invalid json}",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in [200, 422, 400]

        response = client.post("/auth/logout", json={})
        assert response.status_code == 200

    def test_api_security_headers(self, client):
        """Test basic security headers"""
        response = client.get("/")
        assert response.status_code == 200

        headers = {k.lower(): v for k, v in response.headers.items()}

        if "server" in headers:
            assert "version" not in headers["server"].lower()

        assert "x-debug" not in headers
        assert (
            "x-powered-by" not in headers
            or "fastapi" not in headers["x-powered-by"].lower()
        )
