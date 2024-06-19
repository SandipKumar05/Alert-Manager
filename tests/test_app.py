import pytest

from src.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_receive_alert(client):
    response = client.post('/alert', json={"labels":{"alertname": "KubePodCrashLooping"}})
    response.status_code == 200
    response.json == {"status": "received"}
