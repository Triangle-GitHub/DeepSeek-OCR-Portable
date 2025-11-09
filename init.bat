@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo DeepSeek-OCR Portable Environment Initializer
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.12 first.
    echo.
    echo You can download it from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo       Python detected: %PYTHON_VERSION%
echo.

:: Check env directory
if exist ".\env\Scripts\python.exe" (
    echo [2/4] Existing virtual environment detected
    echo       Skipping environment creation
    echo.
) else (
    echo [2/4] Creating virtual environment at .\env ...
    python -m venv env
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo       ✓ Virtual environment created
    echo.
)

:: Activate venv and install dependencies
echo [3/4] Installing Python dependencies...
echo       This may take a few minutes, please wait...
echo.

call .\env\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip --quiet

:: Install PyTorch CUDA build (fallback to CPU if failed)
echo       Installing PyTorch (CUDA 12.8)...
pip install torch==2.9.0+cu128 torchvision==0.24.0+cu128 torchaudio==2.9.0+cu128 --index-url https://download.pytorch.org/whl/cu128 --quiet
if errorlevel 1 (
    echo       [WARN] CUDA build failed, trying CPU build...
    pip install torch torchvision torchaudio --quiet
)

:: Install other dependencies
echo       Installing other dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Dependency installation failed
    pause
    exit /b 1
)

echo       ✓ All dependencies installed
echo.

:: Download models
echo [4/4] Downloading DeepSeek-OCR model files...
echo.

if not exist ".\models" (
    mkdir models
)

python download_models.py
if errorlevel 1 (
    echo.
    echo [WARN] Model download not fully completed
    echo        You can rerun later: python download_models.py
    echo        Or manually download from: https://www.modelscope.cn/models/deepseek-ai/DeepSeek-OCR/files
    echo.
) else (
    echo.
    echo ✓ Model download completed
    echo.
)

:: Done
echo ============================================================
echo Initialization complete!
echo ============================================================
echo.
echo Usage:
echo   1. Run OCR: run_ocr.bat
echo   2. Or activate env manually: .\env\Scripts\activate.bat
echo      then run: python run_ocr.py
echo.
echo To re-download models:
echo   .\env\Scripts\python.exe download_models.py
echo.

pause
