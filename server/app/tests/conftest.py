import os
import pytest
import asyncio
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

# Set ENV to tests before imports
os.environ["ENV"] = "tests"

from main import app
from core.config import settings
from dependencies.db import get_session


# Test database engine
test_engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    echo=False
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup test database with all tables"""
    # Import all models to ensure they are registered with SQLModel
    from models.users.user import User
    from models.areas.area import Area  
    from models.services.service import Service
    from models.services.action import Action
    from models.services.reaction import Reaction
    from models.oauth.oauth_login import OAuthLogin
    
    # Create all tables
    SQLModel.metadata.create_all(test_engine)
    yield
    # Cleanup after tests
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def session():
    """Provide a database session for tests"""
    with Session(test_engine) as session:
        yield session
        session.rollback()


def get_test_session():
    """Override database session for tests"""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client():
    """Provide a test client"""
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def clean_database(session):
    """Clean database between tests"""
    # Clear all tables
    from models.users.user import User
    from models.areas.area import Area
    from models.services.service import Service
    from models.services.action import Action
    from models.services.reaction import Reaction
    from models.oauth.oauth_login import OAuthLogin
    
    session.query(Area).delete()
    session.query(User).delete()
    session.query(Action).delete() 
    session.query(Reaction).delete()
    session.query(Service).delete()
    session.query(OAuthLogin).delete()
    session.commit()
    yield