import pytest

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from tests.conftest import user_token

client = TestClient(app)


@pytest.mark.parametrize(
    "gender, exp_status_code, is_token, is_success",
    [
        ("male", status.HTTP_200_OK, True, True),
        ("invalid", status.HTTP_422_UNPROCESSABLE_ENTITY, True, False),
        ("male", status.HTTP_401_UNAUTHORIZED, False, False)
    ]
)
def test_recommender(gender, exp_status_code, is_token, is_success, user_token):
    if is_token:
        headers = {"Authorization": f"Bearer {user_token}"}
    else:
        headers = None
    response = client.get(
        f"/Recommender/{gender}",
        headers=headers
    )
    assert response.status_code == exp_status_code
    if is_success:
        assert isinstance(response.json()["Activity"], str)
