import os
from typing import List
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib

app = FastAPI(
    title="D2C Personal-Care Customer Churn Scoring Service",
    description="Production-ready FastAPI engine exposing real-time risk predictions for CRM execution tools.",
    version="1.0.0"
)

# 1. Pydantic Input Validation Schema
class CustomerFeatures(BaseModel):
    customer_id: str = Field(..., description="Unique customer identifier token")
    recency_days: int = Field(..., ge=0)
    frequency_180d: int = Field(..., ge=0)
    monetary_180d: float = Field(..., ge=0.0)
    return_rate_180d: float = Field(0.0, ge=0.0, le=1.0)
    avg_discount_pct_180d: float = Field(0.0, ge=0.0, le=1.0)
    avg_rating_180d: float = Field(5.0, ge=1.0, le=5.0)
    category_diversity_180d: int = Field(1, ge=1)
    ticket_count_90d: int = Field(0, ge=0)
    negative_ticket_rate_90d: float = Field(0.0, ge=0.0, le=1.0)
    avg_resolution_hours_90d: float = Field(0.0, ge=0.0)
    days_since_signup: int = Field(..., ge=0)
    sessions_30d: int = Field(0, ge=0)
    product_views_30d: int = Field(0, ge=0)
    cart_adds_30d: int = Field(0, ge=0)
    wishlist_adds_30d: int = Field(0, ge=0)
    abandoned_carts_30d: int = Field(0, ge=0)
    email_opens_30d: int = Field(0, ge=0)
    campaign_clicks_30d: int = Field(0, ge=0)
    last_visit_days_ago: int = Field(..., ge=0)

# Model Artifact Loader
MODEL_PATH = "model.pkl"
if os.path.exists(MODEL_PATH):
    payload = joblib.load(MODEL_PATH)
    clf_model = payload["model"]
    model_features = payload["features"]
else:
    clf_model = None
    model_features = []

def generate_risk_explanation(row: CustomerFeatures, prob: float) -> str:
    reasons = []
    if row.recency_days > 45:
        reasons.append("purchase recency exceeds 45 days")
    if row.ticket_count_90d >= 2:
        reasons.append(f"high customer support ticket volume ({row.ticket_count_90d} tickets)")
    if row.last_visit_days_ago > 20:
        reasons.append("digital browsing inactivity")
        
    if not reasons:
        if prob > 0.5:
            return "Elevated risk driven by combined drop-offs in historical purchase velocities and session volumes."
        return "Customer parameters present stable platform interaction patterns across core channels."
    return f"Elevated risk indicators identified due to: {', '.join(reasons)}."

# 2. API Endpoints Implementation
@app.get("/health")
def health_check():
    if clf_model is None:
        raise HTTPException(status_code=503, detail="Prediction weights are missing or uninitialized.")
    return {"status": "ok"}

@app.post("/predict")
def predict_single(payload: CustomerFeatures):
    if clf_model is None:
        raise HTTPException(status_code=503, detail="Operational inference pipeline is unavailable.")
    
    try:
        input_dict = payload.model_dump()
        df = pd.DataFrame([input_dict])
        df_ordered = df[model_features]
        
        prob = float(clf_model.predict_proba(df_ordered)[0][1])
        pred_class = int(1 if prob >= 0.42 else 0)
        
        risk_level = "low"
        if prob >= 0.70:
            risk_level = "high"
        elif prob >= 0.42:
            risk_level = "medium"
            
        explanation = generate_risk_explanation(payload, prob)
        
        return {
            "customer_id": payload.customer_id,
            "churn_probability": round(prob, 4),
            "predicted_class": pred_class,
            "risk_level": risk_level,
            "risk_explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Exception: {str(e)}")

@app.post("/batch_predict")
def predict_batch(payload_list: List[CustomerFeatures]):
    if clf_model is None:
        raise HTTPException(status_code=503, detail="Operational inference pipeline is unavailable.")
    
    try:
        results = []
        for payload in payload_list:
            res = predict_single(payload)
            results.append(res)
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch Inference Exception: {str(e)}")
