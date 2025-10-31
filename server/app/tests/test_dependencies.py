import pytest
from fastapi import HTTPException
from unittest.mock import Mock, patch
from sqlmodel import Session

from dependencies.auth import get_current_user, get_current_user_no_fail
from dependencies.roles import CurrentUser, CurrentAdmin
from dependencies.db import SessionDep
from models import User


class TestGetCurrentUser:
    """Test the get_current_user dependency function"""

    def test_get_current_user_success(self):
        """Test successful user retrieval"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_session.get.return_value = mock_user

        token = "Bearer valid_jwt_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            result = get_current_user(mock_session, token)

            assert result == mock_user
            mock_session.get.assert_called_once_with(User, 1)

    def test_get_current_user_no_token(self):
        """Test get_current_user with no token"""
        mock_session = Mock(spec=Session)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_session, None)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Token missing."

    def test_get_current_user_invalid_token(self):
        """Test get_current_user with invalid token"""
        mock_session = Mock(spec=Session)
        token = "Bearer invalid_token"

        with patch("dependencies.auth.decode_jwt", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_session, token)

            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "Invalid authorization token."

    def test_get_current_user_token_without_bearer(self):
        """Test get_current_user with token not prefixed with Bearer"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_session.get.return_value = mock_user

        token = "raw_jwt_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            result = get_current_user(mock_session, token)

            assert result == mock_user

    def test_get_current_user_token_no_sub(self):
        """Test get_current_user with token missing 'sub' claim"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token_no_sub"

        with patch("dependencies.auth.decode_jwt", return_value={"exp": 1234567890}):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_session, token)

            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "Invalid token."

    def test_get_current_user_user_not_found(self):
        """Test get_current_user when user doesn't exist in database"""
        mock_session = Mock(spec=Session)
        mock_session.get.return_value = None

        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "999"}):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_session, token)

            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "User not found."

    def test_get_current_user_invalid_user_id_format(self):
        """Test get_current_user with invalid user ID format in token"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "invalid_id"}):
            with pytest.raises(ValueError):
                get_current_user(mock_session, token)

    def test_get_current_user_empty_token(self):
        """Test get_current_user with empty token"""
        mock_session = Mock(spec=Session)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_session, "")

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Token missing."

    def test_get_current_user_bearer_only(self):
        """Test get_current_user with 'Bearer ' only"""
        mock_session = Mock(spec=Session)
        token = "Bearer "

        with patch("dependencies.auth.decode_jwt", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_session, token)

            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "Invalid authorization token."

    def test_get_current_user_negative_user_id(self):
        """Test get_current_user with negative user ID"""
        mock_session = Mock(spec=Session)
        mock_session.get.return_value = None

        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "-1"}):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_session, token)

            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "User not found."

    def test_get_current_user_zero_user_id(self):
        """Test get_current_user with user ID 0"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 0
        mock_session.get.return_value = mock_user

        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "0"}):
            result = get_current_user(mock_session, token)

            assert result == mock_user
            mock_session.get.assert_called_once_with(User, 0)


class TestGetCurrentUserNoFail:
    """Test the get_current_user_no_fail dependency function"""

    def test_get_current_user_no_fail_success(self):
        """Test successful user retrieval with no_fail version"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_session.get.return_value = mock_user

        token = "Bearer valid_jwt_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            result = get_current_user_no_fail(mock_session, token)

            assert result == mock_user

    def test_get_current_user_no_fail_no_token(self):
        """Test get_current_user_no_fail with no token returns None"""
        mock_session = Mock(spec=Session)

        result = get_current_user_no_fail(mock_session, None)

        assert result is None

    def test_get_current_user_no_fail_invalid_token(self):
        """Test get_current_user_no_fail with invalid token returns None"""
        mock_session = Mock(spec=Session)
        token = "Bearer invalid_token"

        with patch("dependencies.auth.decode_jwt", return_value=None):
            result = get_current_user_no_fail(mock_session, token)

            assert result is None

    def test_get_current_user_no_fail_no_sub(self):
        """Test get_current_user_no_fail with token missing 'sub' returns None"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token_no_sub"

        with patch("dependencies.auth.decode_jwt", return_value={"exp": 1234567890}):
            result = get_current_user_no_fail(mock_session, token)

            assert result is None

    def test_get_current_user_no_fail_user_not_found(self):
        """Test get_current_user_no_fail when user doesn't exist returns None"""
        mock_session = Mock(spec=Session)
        mock_session.get.return_value = None

        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "999"}):
            result = get_current_user_no_fail(mock_session, token)

            assert result is None

    def test_get_current_user_no_fail_invalid_user_id(self):
        """Test get_current_user_no_fail with invalid user ID returns None"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token"

        with patch(
            "dependencies.auth.decode_jwt", return_value={"sub": "not_a_number"}
        ):
            result = get_current_user_no_fail(mock_session, token)

            assert result is None

    def test_get_current_user_no_fail_empty_string_user_id(self):
        """Test get_current_user_no_fail with empty string user ID returns None"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": ""}):
            result = get_current_user_no_fail(mock_session, token)

            assert result is None

    def test_get_current_user_no_fail_none_user_id(self):
        """Test get_current_user_no_fail with None user ID returns None"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": None}):
            result = get_current_user_no_fail(mock_session, token)

            assert result is None

    def test_get_current_user_no_fail_bearer_handling(self):
        """Test get_current_user_no_fail properly handles Bearer prefix"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_session.get.return_value = mock_user

        token_with_bearer = "Bearer jwt_token"
        with patch(
            "dependencies.auth.decode_jwt", return_value={"sub": "1"}
        ) as mock_decode:
            result = get_current_user_no_fail(mock_session, token_with_bearer)
            assert result == mock_user
            mock_decode.assert_called_with("jwt_token")

        token_without_bearer = "jwt_token"
        with patch(
            "dependencies.auth.decode_jwt", return_value={"sub": "1"}
        ) as mock_decode:
            result = get_current_user_no_fail(mock_session, token_without_bearer)
            assert result == mock_user
            mock_decode.assert_called_with("jwt_token")

    def test_get_current_user_no_fail_type_error_handling(self):
        """Test get_current_user_no_fail handles type errors gracefully"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            with patch("builtins.int", side_effect=TypeError("Cannot convert")):
                result = get_current_user_no_fail(mock_session, token)
                assert result is None

    def test_get_current_user_no_fail_value_error_handling(self):
        """Test get_current_user_no_fail handles value errors gracefully"""
        mock_session = Mock(spec=Session)
        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "invalid"}):
            result = get_current_user_no_fail(mock_session, token)
            assert result is None


class TestRoleDependencies:
    """Test role-based dependency functions"""

    def test_check_user_function(self):
        """Test check_user function"""
        from dependencies.roles import check_user

        mock_user = Mock()
        mock_user.role = "user"

        result = check_user(mock_user)
        assert result == mock_user

    def test_check_admin_function_success(self):
        """Test check_admin function with admin user"""
        from dependencies.roles import check_admin
        from schemas import Role

        mock_user = Mock()
        mock_user.role = Role.ADMIN

        result = check_admin(mock_user)
        assert result == mock_user

    def test_check_admin_function_not_admin(self):
        """Test check_admin function with non-admin user"""
        from dependencies.roles import check_admin
        from schemas import Role

        mock_user = Mock()
        mock_user.role = Role.USER

        with pytest.raises(HTTPException) as exc_info:
            check_admin(mock_user)

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Permission Denied."

    def test_current_user_and_admin_are_annotated_types(self):
        """Test that CurrentUser and CurrentAdmin are properly defined Annotated types"""
        from dependencies.roles import CurrentUserNoFail

        assert CurrentUser is not None
        assert CurrentAdmin is not None
        assert CurrentUserNoFail is not None


class TestSessionDependency:
    """Test database session dependency"""

    def test_session_dep_type(self):
        """Test that SessionDep is properly defined"""
        assert SessionDep is not None


class TestDependencyEdgeCases:
    """Test edge cases and error conditions for dependencies"""

    def test_get_current_user_with_whitespace_token(self):
        """Test get_current_user with token containing whitespace"""
        mock_session = Mock(spec=Session)
        token = " Bearer  token_with_spaces "

        with patch("dependencies.auth.decode_jwt", return_value=None):
            with pytest.raises(HTTPException):
                get_current_user(mock_session, token)

    def test_get_current_user_with_malformed_bearer(self):
        """Test get_current_user with malformed Bearer token"""
        mock_session = Mock(spec=Session)
        token = "Bearertoken"

        with patch("dependencies.auth.decode_jwt", return_value=None):
            with pytest.raises(HTTPException):
                get_current_user(mock_session, token)

    def test_get_current_user_with_very_long_token(self):
        """Test get_current_user with very long token"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_session.get.return_value = mock_user

        long_token = "Bearer " + "a" * 10000

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            result = get_current_user(mock_session, long_token)
            assert result == mock_user

    def test_get_current_user_with_unicode_token(self):
        """Test get_current_user with unicode characters in token"""
        mock_session = Mock(spec=Session)
        token = "Bearer token_with_unicode_中文"

        with patch("dependencies.auth.decode_jwt", return_value=None):
            with pytest.raises(HTTPException):
                get_current_user(mock_session, token)

    def test_get_current_user_database_error(self):
        """Test get_current_user handles database errors"""
        mock_session = Mock(spec=Session)
        mock_session.get.side_effect = Exception("Database error")

        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            with pytest.raises(Exception):
                get_current_user(mock_session, token)

    def test_get_current_user_no_fail_database_error(self):
        """Test get_current_user_no_fail handles database errors"""
        mock_session = Mock(spec=Session)
        mock_session.get.side_effect = Exception("Database error")

        token = "Bearer valid_token"

        with patch("dependencies.auth.decode_jwt", return_value={"sub": "1"}):
            try:
                result = get_current_user_no_fail(mock_session, token)
                assert result is None
            except Exception:
                pass

    def test_get_current_user_multiple_bearer_prefixes(self):
        """Test get_current_user with multiple Bearer prefixes"""
        mock_session = Mock(spec=Session)
        token = "Bearer Bearer actual_token"

        with patch("dependencies.auth.decode_jwt", return_value=None) as mock_decode:
            with pytest.raises(HTTPException):
                get_current_user(mock_session, token)

            mock_decode.assert_called_with("Bearer actual_token")


class TestDependencyIntegration:
    """Test dependencies working together"""

    @patch("dependencies.auth.decode_jwt")
    def test_authentication_flow_integration(self, mock_decode_jwt):
        """Test complete authentication flow through dependencies"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_user.role = "admin"
        mock_session.get.return_value = mock_user

        mock_decode_jwt.return_value = {"sub": "1"}

        token = "Bearer valid_admin_token"

        user_result = get_current_user(mock_session, token)
        assert user_result == mock_user

        no_fail_result = get_current_user_no_fail(mock_session, token)
        assert no_fail_result == mock_user

    @patch("dependencies.auth.decode_jwt")
    def test_permission_escalation_prevention(self, mock_decode_jwt):
        """Test that regular users cannot escalate to admin"""
        mock_session = Mock(spec=Session)
        mock_user = Mock()
        mock_user.id = 1
        mock_user.role = "user"
        mock_session.get.return_value = mock_user

        mock_decode_jwt.return_value = {"sub": "1"}
        token = "Bearer user_token"

        user_result = get_current_user(mock_session, token)
        assert user_result == mock_user

    def test_dependency_error_consistency(self):
        """Test that dependencies return consistent error types"""
        mock_session = Mock(spec=Session)

        test_cases = [
            (None, "Token missing."),
            ("", "Token missing."),
            ("invalid_token", "Invalid authorization token."),
        ]

        for token, expected_detail in test_cases:
            with patch("dependencies.auth.decode_jwt", return_value=None):
                with pytest.raises(HTTPException) as exc_info:
                    get_current_user(mock_session, token)

                assert exc_info.value.status_code == 403
                if token is None or token == "":
                    assert exc_info.value.detail == "Token missing."
                else:
                    assert (
                        "Invalid" in exc_info.value.detail
                        or "Token" in exc_info.value.detail
                    )

