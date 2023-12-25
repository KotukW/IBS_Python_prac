import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from todo import app

client = TestClient(app)

def test_add_task_success():
    task_data =  [{"task": "Дописать код для упражнения 1.2","status": False},
                  {"task": "сходить покушать", "status": False}]

    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200

def test_add_task_invalid_data():
    invalid_task_data = [{"task": "Новая задача"},
                         {'task': 'Принять таблетки','status': 'неудачно'}]

    response = client.post("/tasks", json=invalid_task_data)
    assert response.status_code == 422
