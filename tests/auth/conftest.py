import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from auth.auth_routes import router as auth_router
import tests.auth.test_auth_container # noqa: F401 — triggers container overrides


@pytest.fixture(autouse=True)
def reset_auth_container():
    tests.auth.test_auth_container.setup_test_auth_container()


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(auth_router)
    return TestClient(app)
