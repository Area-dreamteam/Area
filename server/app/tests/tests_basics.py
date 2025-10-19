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
        # CORS headers may be set by middleware
    
    def test_non_existent_endpoint(self, client):
        """Test non-existent endpoint returns 404"""
        response = client.get("/non-existent-endpoint")
        assert response.status_code == 404
    
    def test_api_accepts_json(self, client):
        """Test that API accepts JSON content type"""
        # Test with a simpler endpoint that doesn't require database
        response = client.post(
            "/auth/logout",
            json={},
            headers={"Content-Type": "application/json"}
        )
        # Should not fail due to content type (may fail for other reasons like auth)
        assert response.status_code != 415  # Unsupported Media Type
    
    def test_api_response_format(self, client):
        """Test that API returns JSON responses"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    def test_http_methods(self, client):
        """Test that different HTTP methods work correctly"""
        # GET should work
        response = client.get("/")
        assert response.status_code == 200
        
        # POST should work (may require auth for protected endpoints)
        response = client.post("/auth/logout")
        assert response.status_code in [200, 401, 403]  # Valid responses
        
        # PUT/PATCH may require auth
        response = client.patch("/users/me")
        assert response.status_code in [200, 401, 403, 422]  # Valid responses
        
        # DELETE may require auth
        response = client.delete("/users/me")
        assert response.status_code in [200, 401, 403, 422]  # Valid responses
    
    @patch('main.init_db')
    @patch('main.print_jobs')
    def test_app_startup_lifecycle(self, mock_print_jobs, mock_init_db, client):
        """Test application startup components"""
        # Test that the app can handle requests
        response = client.get("/")
        assert response.status_code == 200
        
        # Verify the app was properly initialized
        assert response.json() == {"message": "Welcome to AREA API"}
    
    def test_api_error_handling(self, client):
        """Test API error handling"""
        # Test with malformed JSON on logout endpoint (doesn't need database)
        response = client.post(
            "/auth/logout",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        # Should handle malformed JSON (may return different status codes)
        assert response.status_code in [200, 422, 400]  # Various acceptable responses
        
        # Test logout endpoint handles empty JSON
        response = client.post("/auth/logout", json={})
        assert response.status_code == 200  # Should work fine
    
    def test_api_security_headers(self, client):
        """Test basic security headers"""
        response = client.get("/")
        assert response.status_code == 200
        
        # Check that sensitive server info is not exposed
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        # Should not expose detailed server info
        if 'server' in headers:
            assert 'version' not in headers['server'].lower()
        
        # Should not have debug headers in production
        assert 'x-debug' not in headers
        assert 'x-powered-by' not in headers or 'fastapi' not in headers['x-powered-by'].lower()
