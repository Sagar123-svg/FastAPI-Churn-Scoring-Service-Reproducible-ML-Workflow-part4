import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

def create_production_artifact():
    print(">> Generating production model artifact pipeline...")
    np.random.seed(42)
    n_samples = 100

    # Match exact feature array structure from the D2C dataset
    feature_names = [
        "recency_days", "frequency_180d", "monetary_180d", "return_rate_180d",
        "avg_discount_pct_180d", "avg_rating_180d", "category_diversity_180d",
        "ticket_count_90d", "negative_ticket_rate_90d", "avg_resolution_hours_90d",
        "days_since_signup", "sessions_30d", "product_views_30d", "cart_adds_30d",
        "wishlist_adds_30d", "abandoned_carts_30d", "email_opens_30d",
        "campaign_clicks_30d", "last_visit_days_ago"
    ]
    
    X_dummy = pd.DataFrame(np.random.randn(n_samples, len(feature_names)), columns=feature_names)
    y_dummy = np.random.choice([0, 1], size=n_samples)
    
    model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
    model.fit(X_dummy, y_dummy)
    
    payload = {
        "model": model,
        "features": feature_names
    }
    
    joblib.dump(payload, "model.pkl")
    print(">> Successfully created and serialized 'model.pkl'.")

if __name__ == "__main__":
    create_production_artifact()
