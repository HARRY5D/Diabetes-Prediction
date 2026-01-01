# Quick Start Script for Diabetes ML API
# Run this from the diabetes-ml-api directory

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Diabetes ML API - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "1. Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Step 2: Check if virtual environment exists
Write-Host ""
Write-Host "2. Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "   ✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
    Write-Host "   ✅ Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host ""
Write-Host "3. Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "   ✅ Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host ""
Write-Host "4. Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✅ Dependencies installed" -ForegroundColor Green

# Step 5: Check model files
Write-Host ""
Write-Host "5. Checking model files..." -ForegroundColor Yellow
$modelFiles = @(
    "models/pretrained_lasso_champion.joblib",
    "models/pretrained_lasso_champion_rfe.joblib",
    "models/pretrained_lasso_champion_scaler.joblib"
)

$allFilesExist = $true
foreach ($file in $modelFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file NOT FOUND" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "   ⚠️  Some model files are missing!" -ForegroundColor Yellow
    Write-Host "   Please copy model files to the models/ directory" -ForegroundColor Yellow
    exit 1
}

# Step 6: Start the server
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 Starting API Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will start at: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Swagger UI: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
uvicorn app.main:app --reload
