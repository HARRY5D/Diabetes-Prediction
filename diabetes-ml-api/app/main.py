# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import DiabetesInput, PredictionOutput, HealthResponse
from app.inference import predict_diabetes_progression, is_model_loaded, get_model_info
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Diabetes Progression Prediction API",
    description=(
        "Educational ML inference API for predicting diabetes disease progression. "
        "This system uses a trained Lasso regression model with RFE feature selection. "
        "**Note:** This is for educational and demonstration purposes only. "
        "Not intended for clinical or diagnostic use."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware (for web frontend if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("🚀 Starting Diabetes ML API...")
    if is_model_loaded():
        logger.info("✅ Model loaded successfully")
    else:
        logger.error("❌ Model failed to load - check model files")

@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "Diabetes Progression Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "model_info": "/model/info",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint.
    Returns the current status of the API and model.
    """
    return {
        "status": "ok" if is_model_loaded() else "error",
        "model_loaded": is_model_loaded(),
        "version": "1.0.0"
    }

@app.get("/model/info", tags=["Model"])
def model_info():
    """
    Get information about the loaded model.
    Returns model type, selected features, and preprocessing steps.
    """
    if not is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return get_model_info()

@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict(data: DiabetesInput):
    """
    Make a diabetes progression prediction.
    
    **Input:** Normalized feature values (10 features)
    - age: Normalized age (-2.0 to 2.0)
    - sex: Normalized sex (-0.05=Female, 0.05=Male)
    - bmi: Normalized BMI (-2.5 to 3.0)
    - bp: Normalized blood pressure (-2.0 to 3.0)
    - s1-s6: Normalized blood measurements (-2.0 to 3.0)
    
    **Output:** Disease progression prediction
    - prediction: Predicted score (25 to 346)
    - interpretation: Risk level (Low/Moderate/High)
    - note: Usage disclaimer
    
    **Example Request:**
    ```json
    {
        "age": 0.03,
        "sex": 0.05,
        "bmi": 0.06,
        "bp": 0.04,
        "s1": 0.02,
        "s2": 0.03,
        "s3": -0.02,
        "s4": 0.03,
        "s5": 0.05,
        "s6": 0.04
    }
    ```
    """
    if not is_model_loaded():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please check server logs."
        )
    
    try:
        result = predict_diabetes_progression(**data.dict())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(data_list: list[DiabetesInput]):
    """
    Make predictions for multiple patients at once.
    
    **Input:** List of patient data (up to 100 patients)
    **Output:** List of predictions
    """
    if not is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(data_list) > 100:
        raise HTTPException(
            status_code=400,
            detail="Batch size limit: 100 patients per request"
        )
    
    try:
        results = []
        for patient_data in data_list:
            result = predict_diabetes_progression(**patient_data.dict())
            results.append(result)
        return {"predictions": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch prediction failed")

# Run with: uvicorn app.main:app --reload
