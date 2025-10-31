

class TestUsersAPIAuthentication:
    """Test users API authentication requirements"""

    def test_get_current_user_no_auth(self, client):
        """Test getting current user without authentication"""
        response = client.get("/users/me")
        assert response.status_code == 403
        assert response.json()["detail"] == "Token missing."

    def test_delete_current_user_no_auth(self, client):
        """Test deleting current user without authentication"""
        response = client.delete("/users/me")
        assert response.status_code == 403

    def test_update_user_no_auth(self, client):
        """Test updating user without authentication"""
        update_data = {"name": "New Name"}
        response = client.patch("/users/me", json=update_data)
        assert response.status_code == 403

    def test_get_users_no_auth(self, client):
        """Test getting all users without authentication"""
        response = client.get("/users/")
        assert response.status_code == 403

    def test_get_user_by_id_no_auth(self, client):
        """Test getting user by ID without authentication"""
        response = client.get("/users/1")
        assert response.status_code == 403

    def test_delete_user_by_id_no_auth(self, client):
        """Test deleting user by ID without authentication"""
        response = client.delete("/users/1")
        assert response.status_code == 403

    def test_invalid_token_handling(self, client):
        """Test API with invalid token"""
        headers = {"Cookie": "access_token=Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 403
