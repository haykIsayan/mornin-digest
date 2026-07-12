import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from auth.api.auth_middleware import get_current_user
from digest.digest_routes import router as digest_router
import tests.digest.test_digest_container # noqa: F401 — triggers container overrides

TEST_USER_ID = "test-user-123"


def fake_get_current_user():
    return TEST_USER_ID


@pytest.fixture(autouse=True)
def reset_digest_container():
    tests.digest.test_digest_container.setup_test_digest_container()


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(digest_router)
    app.dependency_overrides[get_current_user] = fake_get_current_user
    return TestClient(app)


@pytest.fixture
def test_user_id():
    return TEST_USER_ID
