import logging
import os
from . import text_extractor
# Import Jithin's prediction logic
from app.ml_logic import predict as ml_predictor 
from app.db.models import Resume

logger = logging.getLogger(__name__)

def run_analysis_pipeline(resume: Resume) -> dict:
    """
    Orchestrates the analysis: Load File -> Extract Text -> Predict.
    """
    file_path = resume.file_path
    logger.info(f"Starting ML pipeline for: {file_path}")
    
    try:
        # 1. Validate file existence
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found on disk: {file_path}")

        # 2. Extract Text
        resume_text = text_extractor.extract_text_from_file(file_path)
        
        if not resume_text or not resume_text.strip():
            return {"error": "Could not extract text from file. It might be empty or a scanned image."}

        # 3. Run Jithin's ML Prediction
        # This calls the 'run_inference_on_text' function in app/ml_logic/predict.py
        analysis_result = ml_predictor.run_inference_on_text(resume_text)
        
        logger.info("ML inference completed successfully.")
        return analysis_result

    except Exception as e:
        logger.error(f"Pipeline Error: {e}")
        return {
            "parsed": {},
            "features": {},
            "score": {"label": 0, "confidence": 0.0, "error": str(e)}
        }