@echo off
setlocal enabledelayedexpansion

:: Get the directory where the script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo ============================================================
echo DeepSeek-OCR Portable Initializer
echo ============================================================
echo.

:: Check env directory
if not exist "%SCRIPT_DIR%env\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo This portable package requires the pre-built 'env' folder.
    echo Please download the complete package from our repository:
    echo   https://github.com/Triangle-GitHub/DeepSeek-OCR-Portable
    echo.
    echo Do NOT try to create environment manually - it will not work.
    echo.
    pause
    exit /b 1
)

:: Install dependencies using env Python
echo [1/2] Checking and installing Python dependencies...
echo       This may take a few minutes, please wait...
echo.

echo       Upgrading pip...
"%SCRIPT_DIR%env\python.exe" -m pip install --upgrade pip --quiet --no-warn-script-location

echo       Installing PyTorch (CUDA 12.8)...
"%SCRIPT_DIR%env\python.exe" -m pip install torch==2.9.0+cu128 torchvision==0.24.0+cu128 torchaudio==2.9.0+cu128 --index-url https://download.pytorch.org/whl/cu128 --no-warn-script-location
if errorlevel 1 (
    echo [ERROR] PyTorch CUDA installation failed. This application requires CUDA support.
    pause
    exit /b 1
)

echo       Installing other dependencies...
"%SCRIPT_DIR%env\python.exe" -m pip install -r requirements.txt --quiet --no-warn-script-location
if errorlevel 1 (
    echo [ERROR] Dependency installation failed
    pause
    exit /b 1
)

echo       All dependencies installed
echo.

:: Download models
echo [2/2] Checking and downloading DeepSeek-OCR model files...
echo.

set MODELS_DIR=%SCRIPT_DIR%models\DeepSeek-OCR

:: Create models directory if not exists
if not exist "%MODELS_DIR%" (
    mkdir "%MODELS_DIR%"
)

:: Run external Python script to check model files
echo       Verifying existing model files...
"%SCRIPT_DIR%env\python.exe" check_model_files.py >nul 2>&1

:: Check return code
if %errorlevel% EQU 0 (
    echo       All model files already exist. Skipping download.
    echo.
) else if %errorlevel% EQU 1 (
    echo       Some files missing or incomplete. Starting download...
    echo.
    "%SCRIPT_DIR%env\python.exe" download_model_files.py
    if errorlevel 1 (
        echo.
        echo [WARN] Model download not fully completed
        echo        You can rerun later: "%SCRIPT_DIR%env\python.exe" download_model_files.py
        echo        Or manually download from: https://www.modelscope.cn/models/deepseek-ai/DeepSeek-OCR/files
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo Model download completed
        echo.
    )
) else (
    echo       Unexpected error when checking models. Re-downloading to be safe...
    echo.
    "%SCRIPT_DIR%env\python.exe" download_model_files.py
    if errorlevel 1 (
        echo.
        echo [WARN] Model download not fully completed
        echo        You can rerun later: "%SCRIPT_DIR%env\python.exe" download_model_files.py
        echo        Or manually download from: https://www.modelscope.cn/models/deepseek-ai/DeepSeek-OCR/files
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo Model download completed
        echo.
    )
)



:: Done
echo Initialization complete!
echo.
echo ============================================================
"%SCRIPT_DIR%env\python.exe" run_ocr.py
