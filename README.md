# Diabetes Disease Progression Prediction

## Overview
A machine learning project for predicting diabetes disease progression using the scikit-learn diabetes dataset. This project demonstrates end-to-end ML pipeline development, from data exploration to model deployment via REST API.

## Features
- **Multiple ML Models**: Linear Regression, Ridge, Lasso, ElasticNet, Decision Tree, Random Forest, Gradient Boosting, and SVR
- **Advanced Feature Engineering**: Interaction features (BMI×BP, LDL/HDL ratio, Age×BMI)
- **Feature Selection**: Recursive Feature Elimination (RFE) for optimal feature selection
- **Hyperparameter Tuning**: GridSearchCV and RandomizedSearchCV with cross-validation
- **REST API**: Production-ready FastAPI service for real-time predictions
- **Model Persistence**: Serialized models with joblib for deployment

## Project Structure
```
Diabetes-Prediction/
├── diabetes-ml-api/              # FastAPI REST API
│   ├── app/
│   │   ├── main.py              # API endpoints
│   │   ├── inference.py         # ML inference logic
│   │   └── schemas.py           # Request/response models
│   └── models/                   # Trained model artifacts
├── models/                       # Saved model files
├── diab_mlops.ipynb             # Initial ML pipeline
├── diabetes_progression_comprehensive.ipynb
├── final_diab_mlops.ipynb       # Complete ML pipeline
└── first.ipynb                   # EDA notebook
```

## Model Performance
- **Best Model**: Lasso Regression with RFE
- **R² Score**: 0.5911 (explains 59.11% of variance)
- **RMSE**: 43.08
- **Selected Features**: 6 out of 10 (sex, bmi, bp, s1, s2, s5)

## Installation

### Requirements
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/HARRY5D/Diabetes-Prediction.git
cd Diabetes-Prediction

# Install dependencies
pip install numpy pandas scikit-learn matplotlib seaborn joblib

# For API deployment
cd diabetes-ml-api
pip install -r requirements.txt
```

## Usage

### Running Jupyter Notebooks
```bash
jupyter notebook final_diab_mlops.ipynb
```

### Running the API
```bash
cd diabetes-ml-api
uvicorn app.main:app --reload
```

Access the API at:
- **API Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

### Making Predictions
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "age": 0.03, "sex": 0.05, "bmi": 0.06, "bp": 0.04,
           "s1": 0.02, "s2": 0.03, "s3": -0.02, "s4": 0.03,
           "s5": 0.05, "s6": 0.04
         }'
```

## Dataset
- **Source**: [Scikit-learn Diabetes Dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset)
- **Samples**: 442
- **Features**: 10 (age, sex, BMI, blood pressure, 6 blood serum measurements)
- **Target**: Quantitative measure of disease progression one year after baseline

## Feature Descriptions
All features are normalized (mean-centered and scaled):
- **age**: Age in years
- **sex**: Gender
- **bmi**: Body mass index
- **bp**: Average blood pressure
- **s1**: Total serum cholesterol
- **s2**: Low-density lipoproteins (LDL)
- **s3**: High-density lipoproteins (HDL)
- **s4**: Total cholesterol / HDL ratio
- **s5**: Serum triglycerides (log scale)
- **s6**: Blood sugar level

## Machine Learning Pipeline
1. **Data Loading & EDA**: Statistical analysis and visualization
2. **Feature Engineering**: Create interaction features
3. **Feature Selection**: RFE to identify most predictive features
4. **Model Training**: Train 8 baseline models
5. **Hyperparameter Tuning**: Optimize best performers
6. **Model Evaluation**: Compare all models and select champion
7. **Model Persistence**: Save best model with preprocessing pipeline
8. **Deployment**: Serve predictions via REST API

## API Endpoints
- `GET /`: API information
- `GET /health`: Health check
- `GET /model/info`: Model metadata
- `POST /predict`: Single prediction
- `POST /predict/batch`: Batch predictions (up to 100)

## Technologies Used
- **ML/Data Science**: NumPy, Pandas, Scikit-learn
- **Visualization**: Matplotlib, Seaborn
- **API Framework**: FastAPI
- **Model Serialization**: Joblib
- **Server**: Uvicorn (ASGI)

## Disclaimer
⚠️ This project is for **educational and demonstration purposes only**. It is not intended for clinical diagnosis or medical decision-making. Always consult qualified healthcare professionals for medical advice.

## References
- Bradley Efron, Trevor Hastie, Iain Johnstone and Robert Tibshirani (2004). "Least Angle Regression", Annals of Statistics.
- Scikit-learn documentation

## License
MIT License

## Author
HARRY5D

---
**Status**: ✅ Production Ready