import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from main import app
from auth.api.auth_middleware import get_current_user
import tests.digest.test_digest_container # noqa: F401 — triggers container overrides
import tests.auth.test_auth_container # noqa: F401 — triggers container overrides

# --- Override auth to skip JWT verification ---
TEST_USER_ID = "test-user-123"


def fake_get_current_user():
    return TEST_USER_ID


app.dependency_overrides[get_current_user] = fake_get_current_user


@pytest.fixture(autouse=True)
def reset_containers():
    tests.digest.test_digest_container.setup_test_digest_container()
    tests.auth.test_auth_container.setup_test_auth_container()

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user_id():
    return TEST_USER_ID