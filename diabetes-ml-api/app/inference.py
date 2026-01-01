# app/inference.py
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load artifacts once (IMPORTANT - loaded at startup)
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    model = joblib.load(BASE_DIR / "models/pretrained_lasso_champion.joblib")
    rfe = joblib.load(BASE_DIR / "models/pretrained_lasso_champion_rfe.joblib")
    scaler = joblib.load(BASE_DIR / "models/pretrained_lasso_champion_scaler.joblib")
    logger.info("✅ All model artifacts loaded successfully")
    MODEL_LOADED = True
except Exception as e:
    logger.error(f"❌ Failed to load model artifacts: {str(e)}")
    model = None
    rfe = None
    scaler = None
    MODEL_LOADED = False

# Target bounds from dataset
MIN_TARGET = 25.0
MAX_TARGET = 346.0

# Feature columns (original 10 features)
FEATURE_COLUMNS = [
    "age", "sex", "bmi", "bp",
    "s1", "s2", "s3", "s4", "s5", "s6"
]

def is_model_loaded():
    """Check if model artifacts are loaded."""
    return MODEL_LOADED

def interpret_prediction(score: float) -> str:
    """
    Interpret the prediction score into a risk level.
    
    Args:
        score: Predicted disease progression score
        
    Returns:
        Risk level interpretation string
    """
    if score < 100:
        return "Low Risk ✅"
    elif score < 175:
        return "Moderate Risk ⚠️"
    else:
        return "High Risk 🔴"

def predict_diabetes_progression(**inputs):
    """
    Predict diabetes progression score (educational use only).
    
    This function applies the same preprocessing pipeline used during training:
    1. Creates DataFrame with 10 original features
    2. Applies RFE (Recursive Feature Elimination) to select top 6 features
    3. Applies StandardScaler for normalization
    4. Makes prediction using trained Lasso model
    
    Args:
        **inputs: Keyword arguments containing all 10 normalized feature values
        
    Returns:
        dict: Contains prediction score, interpretation, and metadata
        
    Raises:
        ValueError: If model is not loaded or inputs are invalid
    """
    if not MODEL_LOADED:
        raise ValueError("Model artifacts not loaded. Please check model files.")
    
    # Validate inputs
    if len(inputs) != 10:
        raise ValueError(f"Expected 10 features, got {len(inputs)}")
    
    # Create DataFrame with exact column order
    input_df = pd.DataFrame([inputs], columns=FEATURE_COLUMNS)
    
    # Apply RFE (reduces to 6 selected features)
    input_rfe = rfe.transform(input_df)
    
    # Apply scaling (standardization)
    input_scaled = scaler.transform(input_rfe)
    
    # Make prediction
    prediction = model.predict(input_scaled)[0]
    
    # Clamp output to valid range
    prediction = np.clip(prediction, MIN_TARGET, MAX_TARGET)
    
    # Interpret result
    interpretation = interpret_prediction(prediction)
    
    logger.info(f"Prediction made: {prediction:.2f} ({interpretation})")
    
    return {
        "prediction": float(prediction),
        "interpretation": interpretation,
        "note": "Relative disease progression score (educational/demo use only)"
    }

def get_model_info():
    """
    Get information about the loaded model.
    
    Returns:
        dict: Model metadata and configuration
    """
    if not MODEL_LOADED:
        return {"error": "Model not loaded"}
    
    # Get selected features from RFE
    feature_mask = rfe.support_
    selected_features = [FEATURE_COLUMNS[i] for i, selected in enumerate(feature_mask) if selected]
    
    return {
        "model_type": type(model).__name__,
        "n_features_original": len(FEATURE_COLUMNS),
        "n_features_selected": len(selected_features),
        "selected_features": selected_features,
        "target_range": f"{MIN_TARGET} to {MAX_TARGET}",
        "preprocessing_steps": ["RFE", "StandardScaler"]
    }
