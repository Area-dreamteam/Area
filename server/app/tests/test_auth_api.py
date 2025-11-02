from models.users.user import User
from core.security import hash_password


class TestRegisterEndpoint:
    """Test /auth/register endpoint"""

    def test_register_success(self, client, session):
        """Test successful user registration"""
        user_data = {"email": "test@example.com", "password": "TestPassword123!"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User registered"
        assert "id" in data
        assert data["email"] == "test@example.com"

    def test_register_email_already_exists(self, client, session):
        """Test registration with existing email"""
        existing_user = User(
            email="existing@example.com",
            password=hash_password("ExistingPassword123!"),
            name="Existing User",
        )
        session.add(existing_user)
        session.commit()

        user_data = {"email": "existing@example.com", "password": "TestPassword123!"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format"""
        user_data = {"email": "invalid-email", "password": "TestPassword123!"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == 422
    
    def test_register_weak_password(self, client):
        """Test registration with weak password (no uppercase)"""
        user_data = {"email": "test@example.com", "password": "testpassword123!"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == 422
    
    def test_register_password_no_special_char(self, client):
        """Test registration with password missing special character"""
        user_data = {"email": "test@example.com", "password": "TestPassword123"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == 422
    
    def test_register_password_too_short(self, client):
        """Test registration with password that is too short"""
        user_data = {"email": "test@example.com", "password": "Test1!"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == 422


class TestLoginEndpoint:
    """Test /auth/login endpoint"""

    def test_login_success(self, client, session):
        """Test successful login"""
        user = User(
            email="login@example.com",
            password=hash_password("TestPassword123!"),
            name="Test User",
        )
        session.add(user)
        session.commit()

        user_data = {"email": "login@example.com", "password": "TestPassword123!"}

        response = client.post("/auth/login", json=user_data)

        assert response.status_code == 200
        assert response.json()["message"] == "Logged successfully"
        assert "access_token" in response.cookies

    def test_login_user_not_found(self, client):
        """Test login with non-existent user"""
        user_data = {"email": "nonexistent@example.com", "password": "TestPassword123!"}

        response = client.post("/auth/login", json=user_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_wrong_password(self, client, session):
        """Test login with wrong password"""
        user = User(
            email="wrong@example.com",
            password=hash_password("CorrectPassword123!"),
            name="Test User",
        )
        session.add(user)
        session.commit()

        user_data = {"email": "wrong@example.com", "password": "WrongPassword123!"}

        response = client.post("/auth/login", json=user_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid credentials"


class TestLogoutEndpoint:
    """Test /auth/logout endpoint"""

    def test_logout_success(self, client):
        """Test successful logout"""
        response = client.post("/auth/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"


class TestAuthenticationFlow:
    """Test complete authentication flows"""

    def test_register_login_logout_flow(self, client, session):
        """Test complete register -> login -> logout flow"""
        user_data = {"email": "flow@example.com", "password": "FlowPassword123!"}

        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 200

        login_response = client.post("/auth/login", json=user_data)
        assert login_response.status_code == 200

        logout_response = client.post("/auth/logout")
        assert logout_response.status_code == 200

