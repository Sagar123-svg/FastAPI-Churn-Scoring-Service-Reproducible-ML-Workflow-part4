import os
import pytest
from fastapi.testclient import TestClient

# Create a local artifact if missing to pass tests successfully
from train_model import create_production_artifact
create_production_artifact()

from app.main import app

client = TestClient(app)

@pytest.fixture
def valid_payload():
    return {
        "customer_id": "CUST99999",
        "recency_days": 12,
        "frequency_180d": 4,
        "monetary_180d": 2500.50,
        "return_rate_180d": 0.1,
        "avg_discount_pct_180d": 0.15,
        "avg_rating_180d": 4.5,
        "category_diversity_180d": 3,
        "ticket_count_90d": 0,
        "negative_ticket_rate_90d": 0.0,
        "avg_resolution_hours_90d": 0.0,
        "days_since_signup": 180,
        "sessions_30d": 12,
        "product_views_30d": 30,
        "cart_adds_30d": 5,
        "wishlist_adds_30d": 2,
        "abandoned_carts_30d": 0,
        "email_opens_30d": 8,
        "campaign_clicks_30d": 3,
        "last_visit_days_ago": 2
    }

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_single_prediction_valid(valid_payload):
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_probability" in data
    assert "predicted_class" in data
    assert data["customer_id"] == "CUST99999"

def test_single_prediction_invalid_bounds(valid_payload):
    # Pass an invalid negative metric to trigger Pydantic bounds validation
    valid_payload["recency_days"] = -5
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422
