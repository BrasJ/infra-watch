import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.db.models import host, snapshot, metric, alert, user

@pytest.fixture(scope='session')
def db_file():
    db_fd, db_path = tempfile.mkstemp()
    yield db_path
    os.close(db_fd)
    try:
        os.remove(db_path)
    except PermissionError:
        pass

@pytest.fixture(scope='session')
def test_engine(db_file):
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_file}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope='function')
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope='function')
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c