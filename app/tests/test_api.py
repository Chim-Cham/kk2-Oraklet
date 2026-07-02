from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

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

def test_upload_invalid_file():
    response = client.post(
        "/data/upload",
        files={
            "file": (
                "notes.txt",
                "hello",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Only CSV allowed"
    }

def test_dataset_stats():

    csv = (
        "name,age\n"
        "Gustav,31\n"
        "Kajsa,35\n"
    )

    client.post(
        "/data/upload",
        files={
            "file": (
                "test.csv",
                csv,
                "text/csv"
            )
        }
    )

    response = client.get("/data/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["dataset"] == "test.csv"
    assert "stats" in body

@patch("app.main.chain")
def test_ai_ask(mock_chain):
    mock_chain.invoke.return_value = {
        "question": "How many rows?",
        "answer": "10",
        "model": "TestModel"
    }

    response = client.post(
        "/ai/ask",
        json={
            "question": "How many rows?"
        }
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "10"