from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Running"
    }

def test_upload_csv():

    csv = (
        "name,age\n"
        "Gustav,31\n"
        "Kajsa,35\n"
    )

    response = client.post(
        "/data/upload",
        files={
            "file": (
                "test.csv",
                csv,
                "text/csv"
            )
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "test.csv"
    