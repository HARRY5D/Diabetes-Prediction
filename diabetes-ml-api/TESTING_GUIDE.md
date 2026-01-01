# 🧪 Complete Testing Guide - Diabetes ML API

## Quick Start

### 1. Start the Server

```bash
cd D:\JAVA\CODE\PYTHON\ML\Diabetes_mlops\diabetes-ml-api
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
🚀 Starting Diabetes ML API...
✅ Model loaded successfully
```

---

## Testing Methods

### Method 1: Browser (Quick Sanity Check)

Open: **http://127.0.0.1:8000/docs**

✅ Interactive Swagger UI appears  
✅ Try `/health` endpoint  
✅ Try `/predict` with example data  

---

## Method 2: Postman Testing (RECOMMENDED)

### 📦 Import Collection

1. Open Postman
2. Click **Import**
3. Use file: `Diabetes_ML_API.postman_collection.json`
4. Collection appears with 5 pre-configured requests

---

### 🧪 Test Cases

#### Test 1: Health Check ✅

**Method:** GET  
**URL:** `http://127.0.0.1:8000/health`

**Expected Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**✅ Pass Criteria:** Status 200, model_loaded = true

---

#### Test 2: Root Endpoint 📋

**Method:** GET  
**URL:** `http://127.0.0.1:8000/`

**Expected Response:**
```json
{
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
```

**✅ Pass Criteria:** Status 200, all endpoints listed

---

#### Test 3: Model Info 🔍

**Method:** GET  
**URL:** `http://127.0.0.1:8000/model/info`

**Expected Response:**
```json
{
  "model_type": "Lasso",
  "n_features_original": 10,
  "n_features_selected": 6,
  "selected_features": ["sex", "bmi", "bp", "s1", "s2", "s5"],
  "target_range": "25.0 to 346.0",
  "preprocessing_steps": ["RFE", "StandardScaler"]
}
```

**✅ Pass Criteria:** Status 200, shows Lasso model with 6 selected features

---

#### Test 4: Single Prediction - Moderate Risk ⚠️

**Method:** POST  
**URL:** `http://127.0.0.1:8000/predict`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
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

**Expected Response:**
```json
{
  "prediction": 206.82,
  "interpretation": "Moderate Risk ⚠️",
  "note": "Relative disease progression score (educational/demo use only)"
}
```

**✅ Pass Criteria:** 
- Status 200
- Prediction between 25-346
- Interpretation = "Moderate Risk ⚠️"

---

#### Test 5: Single Prediction - Low Risk ✅

**Method:** POST  
**URL:** `http://127.0.0.1:8000/predict`

**Body (raw JSON):**
```json
{
  "age": -0.5,
  "sex": -0.05,
  "bmi": -0.3,
  "bp": -0.2,
  "s1": -0.1,
  "s2": -0.1,
  "s3": 0.2,
  "s4": -0.2,
  "s5": -0.1,
  "s6": -0.1
}
```

**Expected Response:**
```json
{
  "prediction": 85.43,
  "interpretation": "Low Risk ✅",
  "note": "Relative disease progression score (educational/demo use only)"
}
```

**✅ Pass Criteria:** 
- Prediction < 100
- Interpretation = "Low Risk ✅"

---

#### Test 6: Single Prediction - High Risk 🔴

**Method:** POST  
**URL:** `http://127.0.0.1:8000/predict`

**Body (raw JSON):**
```json
{
  "age": 1.5,
  "sex": 0.05,
  "bmi": 1.0,
  "bp": 1.0,
  "s1": 0.8,
  "s2": 0.9,
  "s3": -0.5,
  "s4": 0.9,
  "s5": 0.8,
  "s6": 0.8
}
```

**Expected Response:**
```json
{
  "prediction": 252.18,
  "interpretation": "High Risk 🔴",
  "note": "Relative disease progression score (educational/demo use only)"
}
```

**✅ Pass Criteria:** 
- Prediction > 175
- Interpretation = "High Risk 🔴"

---

#### Test 7: Batch Prediction 📦

**Method:** POST  
**URL:** `http://127.0.0.1:8000/predict/batch`

**Body (raw JSON):**
```json
[
  {
    "age": -0.5,
    "sex": -0.05,
    "bmi": -0.3,
    "bp": -0.2,
    "s1": -0.1,
    "s2": -0.1,
    "s3": 0.2,
    "s4": -0.2,
    "s5": -0.1,
    "s6": -0.1
  },
  {
    "age": 0.3,
    "sex": 0.05,
    "bmi": 0.5,
    "bp": 0.4,
    "s1": 0.3,
    "s2": 0.4,
    "s3": -0.3,
    "s4": 0.5,
    "s5": 0.4,
    "s6": 0.3
  },
  {
    "age": 1.5,
    "sex": 0.05,
    "bmi": 1.0,
    "bp": 1.0,
    "s1": 0.8,
    "s2": 0.9,
    "s3": -0.5,
    "s4": 0.9,
    "s5": 0.8,
    "s6": 0.8
  }
]
```

**Expected Response:**
```json
{
  "predictions": [
    {
      "prediction": 85.43,
      "interpretation": "Low Risk ✅",
      "note": "..."
    },
    {
      "prediction": 215.67,
      "interpretation": "Moderate Risk ⚠️",
      "note": "..."
    },
    {
      "prediction": 252.18,
      "interpretation": "High Risk 🔴",
      "note": "..."
    }
  ],
  "count": 3
}
```

**✅ Pass Criteria:** 
- Status 200
- Returns 3 predictions
- Each has different risk level

---

## Method 3: cURL Commands

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Single Prediction
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Model Info
```bash
curl http://127.0.0.1:8000/model/info
```

---

## Method 4: Python Requests

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Prediction
patient_data = {
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

response = requests.post(
    f"{BASE_URL}/predict",
    json=patient_data
)

result = response.json()
print(f"Prediction: {result['prediction']:.2f}")
print(f"Risk: {result['interpretation']}")
```

---

## Error Testing

### Test 8: Invalid Input (Missing Field)

**Body:**
```json
{
  "age": 0.03,
  "sex": 0.05,
  "bmi": 0.06
}
```

**Expected:** Status 422 (Validation Error)

---

### Test 9: Invalid Data Type

**Body:**
```json
{
  "age": "invalid",
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

**Expected:** Status 422 (Validation Error)

---

## Feature Value Ranges

All input features are **normalized** values:

| Feature | Range | Meaning |
|---------|-------|---------|
| age | -2.0 to 2.0 | Younger (-) to Older (+) |
| sex | -0.05 to 0.05 | Female (-0.05) or Male (0.05) |
| bmi | -2.5 to 3.0 | Underweight (-) to Obese (+) |
| bp | -2.0 to 3.0 | Low BP (-) to High BP (+) |
| s1 | -2.0 to 3.0 | Total cholesterol |
| s2 | -2.0 to 3.0 | LDL cholesterol (bad) |
| s3 | -2.0 to 2.0 | HDL cholesterol (good) |
| s4 | -2.0 to 3.0 | Total/HDL ratio |
| s5 | -2.0 to 3.0 | Log triglycerides |
| s6 | -2.0 to 3.0 | Blood sugar |

---

## Risk Interpretation

| Score Range | Risk Level | Interpretation |
|-------------|-----------|----------------|
| < 100 | Low Risk ✅ | Slower disease progression |
| 100-174 | Moderate Risk ⚠️ | Average progression rate |
| ≥ 175 | High Risk 🔴 | Faster progression |

---

## Complete Test Checklist

- [ ] Server starts without errors
- [ ] Health check returns OK
- [ ] Model info shows Lasso with 6 features
- [ ] Low risk prediction works (score < 100)
- [ ] Moderate risk prediction works (100-174)
- [ ] High risk prediction works (≥ 175)
- [ ] Batch prediction processes multiple patients
- [ ] Invalid input returns 422 error
- [ ] Swagger UI accessible at /docs

---

## Performance Benchmarks

Expected response times (local):
- Health check: < 5ms
- Single prediction: < 20ms
- Batch (10 patients): < 100ms
- Batch (100 patients): < 500ms

---

## Troubleshooting

### Issue: "Model not loaded"

**Solution:**
1. Check model files exist in `models/` directory
2. Verify file names match exactly
3. Check file permissions
4. Restart server

### Issue: Port 8000 already in use

**Solution:**
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: Import errors

**Solution:**
```bash
pip install -r requirements.txt
```

---

## Next Steps

✅ All tests passing → **API is production-ready for demo/educational use**  
⚠️ Some tests failing → Check logs and model files  
🚀 Ready to deploy → Consider Docker containerization  

---

**Testing completed successfully?** 🎉  
You can now confidently add this to your resume/portfolio!
