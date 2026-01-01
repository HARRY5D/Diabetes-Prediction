# Diabetes Progression Prediction API

## Overview

This project demonstrates deployment of a trained machine learning regression model as a REST API using FastAPI. The API accepts normalized input features and returns a relative diabetes progression score.

**⚠️ Important:** This system is intended strictly for **educational and demonstration purposes** and is not a clinical or diagnostic tool.

---

## Features

- ✅ REST API with FastAPI framework
- ✅ Trained Lasso regression model (R² = 0.5711)
- ✅ RFE (Recursive Feature Elimination) preprocessing
- ✅ StandardScaler normalization
- ✅ Input validation with Pydantic
- ✅ Interactive API documentation (Swagger UI)
- ✅ Health check endpoint
- ✅ Batch prediction support

---

## Project Structure

```
diabetes-ml-api/
│
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application
│   ├── inference.py         # ML inference logic
│   └── schemas.py           # Request/response schemas
│
├── models/
│   ├── pretrained_lasso_champion.joblib        # Trained model
│   ├── pretrained_lasso_champion_rfe.joblib    # Feature selector
│   └── pretrained_lasso_champion_scaler.joblib # Feature scaler
│
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## Installation

### 1. Prerequisites

- Python 3.8+
- pip package manager

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

### Start the server

From the project root directory:

```bash
uvicorn app.main:app --reload
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
🚀 Starting Diabetes ML API...
✅ Model loaded successfully
INFO:     Application startup complete.
```

### Access the API

- **API Root:** http://127.0.0.1:8000
- **Interactive Docs (Swagger):** http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc):** http://127.0.0.1:8000/redoc

---

## API Endpoints

### 1. Root (`GET /`)

Get API information and available endpoints.

**Example:**
```bash
curl http://127.0.0.1:8000/
```

### 2. Health Check (`GET /health`)

Check if the API and model are running correctly.

**Example:**
```bash
curl http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### 3. Model Info (`GET /model/info`)

Get information about the loaded model.

**Example:**
```bash
curl http://127.0.0.1:8000/model/info
```

**Response:**
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

### 4. Predict (`POST /predict`)

Make a diabetes progression prediction.

**Example Request:**
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

**Response:**
```json
{
  "prediction": 210.34,
  "interpretation": "Moderate Risk ⚠️",
  "note": "Relative disease progression score (educational/demo use only)"
}
```

### 5. Batch Predict (`POST /predict/batch`)

Make predictions for multiple patients (up to 100 per request).

---

## Testing with Postman

### 1. Health Check (GET)

- **Method:** GET
- **URL:** `http://127.0.0.1:8000/health`
- **Expected:** `{"status": "ok", "model_loaded": true, "version": "1.0.0"}`

### 2. Single Prediction (POST)

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**

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

### 3. Test Different Scenarios

**Healthy Patient (Low Risk):**
```json
{
  "age": -0.5, "sex": 0.05, "bmi": -0.3, "bp": -0.2,
  "s1": -0.1, "s2": -0.1, "s3": 0.2, "s4": -0.2,
  "s5": -0.1, "s6": -0.1
}
```

**High Risk Patient:**
```json
{
  "age": 1.5, "sex": 0.05, "bmi": 1.0, "bp": 1.0,
  "s1": 0.8, "s2": 0.9, "s3": -0.5, "s4": 0.9,
  "s5": 0.8, "s6": 0.8
}
```

---

## Feature Descriptions

All input features are **normalized** values from the diabetes dataset:

| Feature | Range | Description |
|---------|-------|-------------|
| `age` | -2.0 to 2.0 | Normalized age (younger to older) |
| `sex` | -0.05 to 0.05 | -0.05 = Female, 0.05 = Male |
| `bmi` | -2.5 to 3.0 | Body mass index (underweight to obese) |
| `bp` | -2.0 to 3.0 | Blood pressure (low to high) |
| `s1` | -2.0 to 3.0 | Total serum cholesterol |
| `s2` | -2.0 to 3.0 | LDL cholesterol (bad) |
| `s3` | -2.0 to 2.0 | HDL cholesterol (good) |
| `s4` | -2.0 to 3.0 | Total cholesterol / HDL ratio |
| `s5` | -2.0 to 3.0 | Log of serum triglycerides |
| `s6` | -2.0 to 3.0 | Blood sugar level |

**Note:** Values around 0 represent average. Higher values indicate elevated levels.

---

## Model Performance

- **Algorithm:** Lasso Regression with RFE
- **R² Score:** 0.5711 (explains 57.11% of variance)
- **RMSE:** 43.08
- **Selected Features:** 6 out of 10 (sex, bmi, bp, s1, s2, s5)
- **Preprocessing:** RFE + StandardScaler

---

## Troubleshooting

### Model files not found

**Error:** `❌ Failed to load model artifacts`

**Solution:** Ensure model files exist in `models/` directory:
- `pretrained_lasso_champion.joblib`
- `pretrained_lasso_champion_rfe.joblib`
- `pretrained_lasso_champion_scaler.joblib`

### Port already in use

**Error:** `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`

**Solution:** Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Dependencies not installed

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Install requirements:
```bash
pip install -r requirements.txt
```

---

## Deployment Considerations

### For Production (when ready):

1. **Remove `--reload`** flag
2. **Configure CORS** properly in `main.py`
3. **Add authentication** (API keys, JWT)
4. **Use HTTPS** with SSL certificates
5. **Set up logging** to files
6. **Add rate limiting** (e.g., with slowapi)
7. **Use production ASGI server** (e.g., gunicorn with uvicorn workers)
8. **Add monitoring** (health checks, metrics)

---

## License & Disclaimer

**Educational Use Only**

This project is for educational and demonstration purposes. The model and API are not intended for clinical diagnosis, treatment decisions, or medical advice. Always consult qualified healthcare professionals for medical concerns.

---

## Resume Alignment

This project demonstrates:

✅ **ML Model Deployment:** Converting trained models into production-ready REST APIs  
✅ **API Development:** Building scalable APIs with FastAPI and proper validation  
✅ **MLOps Practices:** Model versioning, preprocessing pipelines, and inference optimization  
✅ **Software Engineering:** Clean code structure, documentation, and testing  

Aligns perfectly with:
- Your diabetes ML project
- Your TTS API experience (FastAPI)
- Your ML + MLOps trajectory

---

## Author

Created as part of a comprehensive ML/MLOps portfolio demonstrating end-to-end machine learning system development.

---

## Next Steps

1. ✅ Run the API locally
2. ✅ Test with Postman
3. ✅ Explore Swagger UI at `/docs`
4. 🚀 Consider containerization (Docker)
5. 🚀 Set up CI/CD pipeline
6. 🚀 Deploy to cloud (AWS, Azure, GCP)

---

**Questions or issues?** Check the logs or review the code in `app/` directory.
