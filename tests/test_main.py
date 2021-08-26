from starlette.testclient import TestClient

from file_storage.main import app

client = TestClient(app)


def test_sum():
    response = client.post('/v1/sum', params=[('a', 53), ('b', -21)])
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['result'] == 53 - 21
