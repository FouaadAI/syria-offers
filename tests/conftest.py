import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import ARRAY

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.api.v1 import auth, bookings, categories, offers, payments, uploads  # noqa: E402
from app.core.database import Base, get_db  # noqa: E402
from app.models import booking, merchant, offer, user  # noqa: F401,E402

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_api.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@compiles(ARRAY, "sqlite")
def _compile_array_for_sqlite(_type, _compiler, **_kw):
    return "TEXT"


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(categories.router, prefix="/api/v1")
    app.include_router(offers.router, prefix="/api/v1")
    app.include_router(bookings.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(payments.router, prefix="/api/v1")
    app.include_router(uploads.router, prefix="/api/v1")
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def db_session(client):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
