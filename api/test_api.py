import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.main import app

client = TestClient(app)

valid_payload = {
    "customerid": "TEST-123",
    "country": "United States",
    "state": "California",
    "city": "Los Angeles",
    "zip_code": 90001,
    "lat_long": "33.973616, -118.242766",
    "latitude": 33.973616,
    "longitude": -118.242766,
    "gender": "Female",
    "senior_citizen": "No",
    "partner": "Yes",
    "dependents": "Yes",
    "tenure_months": 24,
    "phone_service": "Yes",
    "multiple_lines": "No",
    "internet_service": "DSL",
    "online_security": "Yes",
    "online_backup": "Yes",
    "device_protection": "No",
    "tech_support": "Yes",
    "streaming_tv": "No",
    "streaming_movies": "No",
    "contract": "One year",
    "paperless_billing": "No",
    "payment_method": "Credit card (automatic)",
    "monthly_charges": 65.5,
    "total_charges": 1572.0,
    "cltv": 4500.0
}

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

def test_valid_prediction():
    with TestClient(app) as client:
        response = client.post("/predict", json=valid_payload)
        assert response.status_code == 200
        data = response.json()
        assert "churn_probability" in data
        assert "risk_level" in data
        assert "top_risk_factor" in data
        assert "protective_factors" in data
        assert "recommended_action" in data
        assert data["customer_id"] == "TEST-123"

def test_missing_fields():
    invalid_payload = valid_payload.copy()
    del invalid_payload["tenure_months"]  # Missing required field
    
    with TestClient(app) as client:
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 422  # Unprocessable Entity
        assert "detail" in response.json()

def test_invalid_values():
    invalid_payload = valid_payload.copy()
    invalid_payload["monthly_charges"] = "NOT_A_FLOAT"
    
    with TestClient(app) as client:
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 422

def test_malformed_input():
    with TestClient(app) as client:
        response = client.post("/predict", data="Not JSON")
        assert response.status_code == 422

def test_batch_prediction():
    with TestClient(app) as client:
        batch = [valid_payload, valid_payload]
        response = client.post("/predict/batch", json=batch)
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 2
