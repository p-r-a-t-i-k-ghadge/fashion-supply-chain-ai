import sys
import os
import pytest
from fastapi.testclient import TestClient

# Embed system boundaries natively pointing structural roots correctly mapping core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

# Emulates explicit terminal network arrays
client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "Operational" in response.json()["status"]

def test_get_products_endpoint():
    response = client.get("/api/v1/products?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "sku" in data[0]
        assert "name" in data[0]

def test_predict_risk_endpoint():
    # Evaluate dynamic database execution logic parameters mapping `product_id=1` exactly
    response = client.get("/api/v1/predict/risk/1")
    if response.status_code == 200:
        data = response.json()
        assert "risk_level" in data
        assert "action_recommended" in data
        assert data["product_id"] == 1
    elif response.status_code == 404:
        # Valid execution boundary indicating SQL data currently missing naturally
        assert response.json()["detail"] == "Product ID boundary unmapped in database constraints."
    else:
        pytest.fail(f"Unexpected structural sequence breakdown: {response.status_code}")

def test_predict_demand_endpoint():
    response = client.get("/api/v1/predict/demand/1")
    assert response.status_code == 200
    data = response.json()
    assert "predicted_demand" in data
    assert "forecast_date" in data
    assert data["product_id"] == 1
