import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from src.api.app import app, get_db
from src.api.database import db_session_maker


@pytest.fixture()
def session():
    """Create session object"""
    session = db_session_maker("sqlite://")
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(session: Session):
    """create test client"""

    def override_get_db():
        return session

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
