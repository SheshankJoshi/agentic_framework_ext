import pytest
from fastapi.testclient import TestClient
from agentic_framework.src.main import app

client = TestClient(app)


def test_home_status_code():
    response = client.get("/")
    assert response.status_code == 200
    print("test passed successfully")


def test_home_content():
    response = client.get("/")
    json_data = response.json()
    expected = {
        "message": "Hello, World! This is Agentic Framework simple server using FastAPI."}
    assert json_data == expected
