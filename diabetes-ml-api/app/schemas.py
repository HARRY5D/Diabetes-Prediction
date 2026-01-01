# app/schemas.py
from pydantic import BaseModel, Field

class DiabetesInput(BaseModel):
    """
    Input schema for diabetes progression prediction.
    All values are normalized features from the diabetes dataset.
    """
    age: float = Field(..., description="Normalized age value")
    sex: float = Field(..., description="Normalized sex value (-0.05=Female, 0.05=Male)")
    bmi: float = Field(..., description="Normalized BMI value")
    bp: float = Field(..., description="Normalized blood pressure value")
    s1: float = Field(..., description="Normalized total serum cholesterol")
    s2: float = Field(..., description="Normalized LDL cholesterol")
    s3: float = Field(..., description="Normalized HDL cholesterol")
    s4: float = Field(..., description="Normalized total cholesterol / HDL ratio")
    s5: float = Field(..., description="Normalized log of serum triglycerides")
    s6: float = Field(..., description="Normalized blood sugar level")
    
    class Config:
        schema_extra = {
            "example": {
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
        }

class PredictionOutput(BaseModel):
    """
    Output schema for prediction response.
    """
    prediction: float = Field(..., description="Predicted disease progression score")
    interpretation: str = Field(..., description="Risk level interpretation")
    note: str = Field(..., description="Disclaimer and usage information")
    
    class Config:
        schema_extra = {
            "example": {
                "prediction": 210.34,
                "interpretation": "Moderate Risk",
                "note": "Relative disease progression score (educational/demo use only)"
            }
        }

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    version: str
