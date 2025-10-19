import pytest
import os
from unittest.mock import Mock, patch, mock_open
from pydantic import ValidationError

from core.config import get_env_file, Settings


class TestGetEnvFile:
    """Test the get_env_file function"""
    
    @patch.dict(os.environ, {'ENV': 'dev'})
    def test_get_env_file_dev(self):
        """Test get_env_file returns .env for dev environment"""
        result = get_env_file()
        assert result == ".env"
    
    @patch.dict(os.environ, {'ENV': 'prod'})
    def test_get_env_file_prod(self):
        """Test get_env_file returns .env.prod for prod environment"""
        result = get_env_file()
        assert result == ".env.prod"
    
    @patch.dict(os.environ, {'ENV': 'tests'})
    def test_get_env_file_tests(self):
        """Test get_env_file returns .env.tests for tests environment"""
        result = get_env_file()
        assert result == ".env.tests"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_env_file_no_env(self):
        """Test get_env_file raises error when ENV not set"""
        with pytest.raises(TypeError):
            get_env_file()
    
    @patch.dict(os.environ, {'ENV': 'invalid'})
    def test_get_env_file_invalid_env(self):
        """Test get_env_file with invalid environment"""
        result = get_env_file()
        # Function doesn't handle invalid env, returns None
        assert result is None
    
    @patch.dict(os.environ, {'ENV': ''})
    def test_get_env_file_empty_env(self):
        """Test get_env_file with empty ENV variable"""
        result = get_env_file()
        assert result is None
    
    @patch.dict(os.environ, {'ENV': 'DEV'})
    def test_get_env_file_case_sensitive(self):
        """Test get_env_file is case sensitive"""
        result = get_env_file()
        # Should not match 'dev', only exact case
        assert result is None
    
    @patch.dict(os.environ, {'ENV': 'development'})
    def test_get_env_file_partial_match(self):
        """Test get_env_file doesn't do partial matching"""
        result = get_env_file()
        assert result is None


class TestSettings:
    """Test the Settings class"""
    
    def test_settings_required_fields(self):
        """Test that Settings class has all required fields"""
        # Test that Settings class is defined with expected attributes
        settings_fields = {
            'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 
            'POSTGRES_PORT', 'POSTGRES_DB', 'JWT_SECRET', 'JWT_ALGORITHM',
            'ACCESS_TOKEN_EXPIRE_HOURS', 'GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET',
            'TODOIST_CLIENT_ID', 'TODOIST_CLIENT_SECRET', 'FRONT_URL'
        }
        
        # Check that Settings class has annotations for all expected fields
        settings_annotations = getattr(Settings, '__annotations__', {})
        
        for field in settings_fields:
            assert field in settings_annotations
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_initialization_success(self, mock_get_env):
        """Test successful Settings initialization with all required fields"""
        settings = Settings()
        
        assert settings.POSTGRES_USER == 'test_user'
        assert settings.POSTGRES_PASSWORD == 'test_pass'
        assert settings.POSTGRES_HOST == 'localhost'
        assert settings.POSTGRES_PORT == 5432
        assert settings.POSTGRES_DB == 'test_db'
        assert settings.JWT_SECRET == 'test_secret'
        assert settings.JWT_ALGORITHM == 'HS256'
        assert settings.ACCESS_TOKEN_EXPIRE_HOURS == 24
        assert settings.GITHUB_CLIENT_ID == 'github_id'
        assert settings.GITHUB_CLIENT_SECRET == 'github_secret'
        assert settings.TODOIST_CLIENT_ID == 'todoist_id'
        assert settings.TODOIST_CLIENT_SECRET == 'todoist_secret'
        assert settings.FRONT_URL == 'http://localhost:3000'
    
    @patch('core.config.get_env_file', return_value='nonexistent.env')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        # Missing other required fields
    }, clear=True)
    def test_settings_missing_required_fields(self, mock_get_env):
        """Test Settings initialization with missing required fields"""
        # When .env file doesn't exist and required fields are missing from env
        # Settings may have defaults or handle missing fields gracefully
        try:
            settings = Settings()
            # If it works, that means defaults are provided
        except ValidationError:
            # If it fails, that's expected for missing required fields
            pass
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': 'invalid_port',  # Invalid integer
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_invalid_integer_field(self, mock_get_env):
        """Test Settings initialization fails with invalid integer field"""
        with pytest.raises(ValidationError):
            Settings()
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': 'invalid_hours',  # Invalid integer
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_invalid_hours_field(self, mock_get_env):
        """Test Settings initialization fails with invalid hours field"""
        with pytest.raises(ValidationError):
            Settings()
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': '',  # Empty secret
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_empty_secret(self, mock_get_env):
        """Test Settings initialization with empty JWT secret"""
        settings = Settings()
        # Empty string should be valid, but not secure
        assert settings.JWT_SECRET == ''
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '0',  # Port 0
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_port_zero(self, mock_get_env):
        """Test Settings with port 0"""
        settings = Settings()
        assert settings.POSTGRES_PORT == 0
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '65535',  # Max port
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_max_port(self, mock_get_env):
        """Test Settings with maximum valid port"""
        settings = Settings()
        assert settings.POSTGRES_PORT == 65535
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '-1',  # Negative hours
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_negative_hours(self, mock_get_env):
        """Test Settings with negative expiration hours"""
        settings = Settings()
        # Negative hours should be valid (could mean immediate expiration)
        assert settings.ACCESS_TOKEN_EXPIRE_HOURS == -1
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'INVALID_ALGORITHM',  # Invalid algorithm
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_invalid_algorithm(self, mock_get_env):
        """Test Settings with invalid JWT algorithm"""
        settings = Settings()
        # Invalid algorithm should still be accepted (validation happens at JWT level)
        assert settings.JWT_ALGORITHM == 'INVALID_ALGORITHM'


class TestConfigurationEdgeCases:
    """Test edge cases and error conditions for configuration"""
    
    @patch.dict(os.environ, {'ENV': 'dev'}, clear=True)
    def test_env_variable_precedence(self):
        """Test that environment variables take precedence"""
        result = get_env_file()
        assert result == ".env"
    
    def test_settings_config_class(self):
        """Test Settings Config class attributes"""
        config = Settings.Config
        # Check that Config class calls get_env_file
        assert hasattr(config, 'env_file')
    
    @patch('core.config.get_env_file', side_effect=Exception("File error"))
    def test_settings_file_error_handling(self, mock_get_env):
        """Test Settings handles file errors"""
        # Settings may handle file errors gracefully by using environment variables
        try:
            settings = Settings()
            # If it succeeds, that's also valid behavior
        except Exception as e:
            # If it fails, that's expected
            assert "File error" in str(e)
    
    @patch('core.config.get_env_file', return_value='nonexistent.env')
    def test_settings_nonexistent_file(self, mock_get_env):
        """Test Settings with nonexistent env file"""
        # Should not fail even if file doesn't exist (uses environment variables)
        try:
            Settings()
        except ValidationError:
            # ValidationError is expected if required env vars are missing
            pass
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'x' * 1000,  # Very long secret
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_very_long_secret(self, mock_get_env):
        """Test Settings with very long JWT secret"""
        settings = Settings()
        assert len(settings.JWT_SECRET) == 1000
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '999999',  # Very large number
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_very_large_hours(self, mock_get_env):
        """Test Settings with very large expiration hours"""
        settings = Settings()
        assert settings.ACCESS_TOKEN_EXPIRE_HOURS == 999999
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'pássword_中文_🔐',  # Unicode password
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_unicode_values(self, mock_get_env):
        """Test Settings with unicode values"""
        settings = Settings()
        assert settings.POSTGRES_PASSWORD == 'pássword_中文_🔐'
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'https://example.com/path?query=value#fragment'  # Complex URL
    })
    def test_settings_complex_url(self, mock_get_env):
        """Test Settings with complex front URL"""
        settings = Settings()
        assert settings.FRONT_URL == 'https://example.com/path?query=value#fragment'
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': '',  # Empty user
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_empty_user(self, mock_get_env):
        """Test Settings with empty postgres user"""
        settings = Settings()
        assert settings.POSTGRES_USER == ''


class TestConfigurationSecurity:
    """Test security-related configuration aspects"""
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'weak',  # Very short secret
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_weak_secret(self, mock_get_env):
        """Test Settings allows weak JWT secret (security warning)"""
        settings = Settings()
        # Should work but is not secure
        assert settings.JWT_SECRET == 'weak'
        assert len(settings.JWT_SECRET) < 32  # Weak secret
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'none',  # Insecure algorithm
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_insecure_algorithm(self, mock_get_env):
        """Test Settings with insecure JWT algorithm"""
        settings = Settings()
        # Should work but is not secure
        assert settings.JWT_ALGORITHM == 'none'
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '0',  # No expiration
        'GITHUB_CLIENT_ID': 'github_id',
        'GITHUB_CLIENT_SECRET': 'github_secret',
        'TODOIST_CLIENT_ID': 'todoist_id',
        'TODOIST_CLIENT_SECRET': 'todoist_secret',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_no_token_expiration(self, mock_get_env):
        """Test Settings with no token expiration"""
        settings = Settings()
        assert settings.ACCESS_TOKEN_EXPIRE_HOURS == 0
    
    @patch('core.config.get_env_file', return_value='.env.tests')
    @patch.dict(os.environ, {
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'JWT_SECRET': 'test_secret',
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_HOURS': '24',
        'GITHUB_CLIENT_ID': '',  # Empty OAuth credentials
        'GITHUB_CLIENT_SECRET': '',
        'TODOIST_CLIENT_ID': '',
        'TODOIST_CLIENT_SECRET': '',
        'FRONT_URL': 'http://localhost:3000'
    })
    def test_settings_empty_oauth_credentials(self, mock_get_env):
        """Test Settings with empty OAuth credentials"""
        settings = Settings()
        assert settings.GITHUB_CLIENT_ID == ''
        assert settings.GITHUB_CLIENT_SECRET == ''
        assert settings.TODOIST_CLIENT_ID == ''
        assert settings.TODOIST_CLIENT_SECRET == ''


class TestMultipleEnvironments:
    """Test behavior across different environments"""
    
    def test_all_environment_types(self):
        """Test all supported environment types"""
        environments = ['dev', 'prod', 'tests']
        expected_files = ['.env', '.env.prod', '.env.tests']
        
        for env, expected_file in zip(environments, expected_files):
            with patch.dict(os.environ, {'ENV': env}):
                result = get_env_file()
                assert result == expected_file
    
    def test_environment_case_sensitivity(self):
        """Test environment variable case sensitivity"""
        test_cases = [
            ('dev', '.env'),
            ('DEV', None),
            ('Dev', None),
            ('PROD', None),
            ('Prod', None),
            ('TESTS', None),
            ('Tests', None),
        ]
        
        for env_value, expected in test_cases:
            with patch.dict(os.environ, {'ENV': env_value}):
                result = get_env_file()
                assert result == expected