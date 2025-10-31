

class TestCompleteUserWorkflow:
    """Test complete user registration and login workflow"""

    def test_complete_user_lifecycle(self, client, session):
        """Test complete user lifecycle: register -> login"""
        user_data = {"email": "integration@example.com", "password": "testpassword123"}

        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 200
        register_data = register_response.json()
        assert register_data["message"] == "User registered"
        assert register_data["email"] == "integration@example.com"

        login_response = client.post("/auth/login", json=user_data)
        assert login_response.status_code == 200
        assert login_response.json()["message"] == "Logged successfully"
        assert "access_token" in login_response.cookies

    def test_duplicate_registration_prevention(self, client, session):
        """Test that duplicate registration is properly prevented"""
        user_data = {"email": "duplicate@example.com", "password": "testpassword123"}

        first_response = client.post("/auth/register", json=user_data)
        assert first_response.status_code == 200

        second_response = client.post("/auth/register", json=user_data)
        assert second_response.status_code == 400
        assert second_response.json()["detail"] == "Email already registered"

    def test_invalid_credentials_handling(self, client):
        """Test handling of invalid login credentials"""
        login_data = {"email": "nonexistent@example.com", "password": "anypassword"}

        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid credentials"


class TestBasicAPIAccess:
    """Test basic API accessibility"""

    def test_api_root_endpoint(self, client):
        """Test that API root endpoint is accessible"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Welcome to AREA API"

    def test_protected_endpoints_without_authentication(self, client):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            ("/users/me", "GET"),
            ("/users/", "GET"),
        ]

        for endpoint, method in protected_endpoints:
            if method == "GET":
                response = client.get(endpoint)

            assert response.status_code == 403

