import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from todo import app

client = TestClient(app)

def test_update_task_success():
    task_data = {"task": "Обновленная задача", "status": True}
    response = client.put("/tasks/10", json=task_data)
    assert response.status_code == 200

def test_update_task_not_found():
    task_data = {"task": "Обновленная задача", "status": True}
    response = client.put("/tasks/100", json=task_data)
    assert response.status_code == 422

def test_update_invalid_data():
    task_data = {'task': 'Дописать код для упражнения 1.3','status': "Выполнено"}
    response = client.put("/tasks/1", json=task_data)
    assert response.status_code == 424