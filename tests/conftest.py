import pytest
from fastapi.testclient import TestClient
from routers.token import ROOT_USERS_DB, get_password_hash

from main import app


TEST_ROOT_USERNAME = "test_root"
TEST_ROOT_PASSWORD = "test_password"

client = TestClient(app)


def pytest_runtest_setup():
    # Add test root user to ROOT_USERS_DB
    if TEST_ROOT_USERNAME not in ROOT_USERS_DB:
        hash_password = get_password_hash(TEST_ROOT_PASSWORD)
        ROOT_USERS_DB[TEST_ROOT_USERNAME] = {
            "username": TEST_ROOT_USERNAME,
            "hashed_password": hash_password,
        }


@pytest.fixture(scope="session")
def root_token() -> str:
    """Get root JWT token"""
    response = client.post(
        "/token/",
        data={
            "username": TEST_ROOT_USERNAME,
            "password": TEST_ROOT_PASSWORD,
        }
    )
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def user_token(root_token) -> str:
    """Get regular user JWT token"""
    token_valid_mins = 10.0
    mins_per_day = 24 * 60.0

    response = client.put(
        "/token/generate",
        headers={"Authorization": f"Bearer {root_token}"},
        json={"username": "test_user",
              "expire_days": token_valid_mins / mins_per_day}
    )
    return response.json()["access_token"]
