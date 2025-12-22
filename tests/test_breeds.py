from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_all_breeds():
    response = client.get("/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], dict)

