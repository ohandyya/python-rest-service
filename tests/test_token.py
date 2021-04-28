import pytest
from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from routers.token import decode_token
from tests.conftest import (
    TEST_ROOT_USERNAME,
    TEST_ROOT_PASSWORD,
    root_token,
    user_token
)

client = TestClient(app)


@pytest.mark.parametrize(
    "username, password, exp_staus_code, exp_keys_list",
    [
        (TEST_ROOT_USERNAME, TEST_ROOT_PASSWORD, status.HTTP_200_OK,
         ["access_token", "token_type"]),
        ("invalid", "invalid", status.HTTP_401_UNAUTHORIZED, None),
    ]
)
def test_login_for_access_token(username, password, exp_staus_code, exp_keys_list):
    response = client.post(
        "/token/",
        data={
            "username": username,
            "password": password,
        }
    )
    assert response.status_code == exp_staus_code
    if exp_keys_list:
        assert all(key in response.json() for key in exp_keys_list)


def test_root_api(root_token):
    response = client.get(
        "/token/root-test",
        headers={"Authorization": f"Bearer {root_token}"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_regular_user_api(user_token):
    response = client.get(
        "/token/reg-test",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_generate_token(root_token):
    username = "test_user"
    token_valid_mins = 10.0
    mins_per_day = 24 * 60.0

    response = client.put(
        "/token/generate",
        headers={"Authorization": f"Bearer {root_token}"},
        json={"username": username,
              "expire_days": token_valid_mins / mins_per_day}
    )

    response_body = response.json()
    assert response_body["token_type"] == "bearer"
    assert isinstance(response_body["access_token"], str)

    # Decode token
    payload = decode_token(response_body["access_token"])
    assert payload["sub"] == username
    assert (payload["exp"] - datetime.utcnow().timestamp()
            ) <= token_valid_mins * 60.0
