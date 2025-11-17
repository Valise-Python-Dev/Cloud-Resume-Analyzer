import json
import os
# The dots (.) below are critical for the files to find each other!
from .parser import parse_text
from .feature_extractor import extract_features
from .scorer import predict as scorer_predict, load_model
from typing import Dict, Any

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

def run_inference_on_text(text: str) -> Dict[str, Any]:
    parsed = parse_text(text)
    feats = extract_features(parsed)
    # attempt to call scorer; handle missing model gracefully
    try:
        score = scorer_predict(feats)
    except FileNotFoundError:
        score = {"label": None, "confidence": None, "error": "Model file not found"}
    except Exception as e:
        score = {"label": None, "confidence": None, "error": str(e)}
        
    output = {
        "parsed": parsed,
        "features": feats,
        "score": score
    }
    return output

def run_from_file(path: str):
    with open(path, "r", encoding="utf8") as f:
        text = f.read()
    return run_inference_on_text(text)