# test_app.py
from fastapi.testclient import TestClient
import sys
import os
import pytest

# Tambahkan direktori induk ke path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_positive():
    response = client.post(
        "/predict",
        json={"text": "saya sangat senang dengan produk ini"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "confidence" in data
    assert isinstance(data["confidence"], float)

def test_predict_negative():
    response = client.post(
        "/predict",
        json={"text": "saya kecewa dengan pelayanan yang buruk"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "confidence" in data

def test_predict_invalid_input():
    response = client.post(
        "/predict",
        json={}
    )
    assert response.status_code != 200  # Should fail

if __name__ == "__main__":
    test_health_check()
    test_predict_positive()
    test_predict_negative()
    test_predict_invalid_input()
    print("All tests passed!")