import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from todo import app

client = TestClient(app)

def test_int_to_rome_success():
    valid_data = [32, 54, 1984, 2024]
    for number in valid_data:
        response = client.post("/int_to_roman", json={"number":number})
        assert response.status_code == 200

def test_int_to_rome_invalid():
    invalid_data = [6000, -10]
    for number in invalid_data:
        response = client.post("/int_to_roman", json={"number": number})
        assert response.status_code == 424