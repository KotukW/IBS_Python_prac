import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from todo import app
client = TestClient(app)

def test_get_task_by_id_success():
    response = client.get("/tasks/3")
    assert response.status_code == 200

def test_get_task_by_id_not_found():
    response = client.get("/tasks/100")
    assert response.status_code == 404