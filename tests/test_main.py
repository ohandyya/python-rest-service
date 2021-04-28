import mock
from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import root_token


from main import app

client = TestClient(app)


def test_welcome():
    response = client.get("/")
    assert response.status_code != status.HTTP_200_OK
    assert response.json() == {"message": "Main application!"}


def test_reset(root_token):
    # Unauthorized
    response = client.get("/reset")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

    # Authorized and success
    response = client.get(
        "/reset",
        headers={"Authorization": f"Bearer {root_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Reset DB success"}


@mock.patch("main.database")
def test_reset_error(mock_database, root_token):
    mock_database.initialize_activity.side_effect = Exception(
        "DB initialization failure")

    response = client.get(
        "/reset",
        headers={"Authorization": f"Bearer {root_token}"}
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"message": "Reset DB fail"}
