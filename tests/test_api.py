from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_amio_api_returns_expected_json():
    resp = client.get("/AMIO-API")
    assert resp.status_code == 200
    data = resp.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    # Quick structural checks
    assert all("timestamp" in item for item in data["data"])
    assert all("label" in item for item in data["data"])
