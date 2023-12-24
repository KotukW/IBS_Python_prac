import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from todo import app

client = TestClient(app)

def test_delete_task_success():
    response = client.delete("/tasks/2")
    assert response.status_code == 200

def test_delete_task_not_found():
    response = client.delete("/tasks/100")
    assert response.status_code == 404

def test_delete_task_invalid_data():
    response = client.delete("/tasks/пять")
    assert response.status_code == 424