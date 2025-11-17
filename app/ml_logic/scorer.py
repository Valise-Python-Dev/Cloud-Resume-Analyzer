import os
import joblib
import pandas as pd
from typing import Dict, Any

# Ensure this points to where you pasted the file: app/ml_logic/models/resume_scorer.joblib
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "resume_scorer.joblib")

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    model, features = joblib.load(MODEL_PATH)
    return model, features

def predict(features: Dict[str, Any]):
    model, feature_list = load_model()
    # Create a DataFrame with 1 row and correct columns
    X = pd.DataFrame([features], columns=feature_list).fillna(0)
    
    score_label = model.predict(X)[0]
    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0].max()
        
    return {"label": int(score_label), "confidence": float(prob) if prob is not None else 0.0}