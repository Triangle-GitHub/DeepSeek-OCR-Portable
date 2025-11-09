@echo off
setlocal EnableDelayedExpansion

:: Get the directory where the script is located
set SCRIPT_DIR=%~dp0

:: Change to script directory
cd /d "%SCRIPT_DIR%"

:: Run the Python script using env Python
"%SCRIPT_DIR%env\python.exe" "%SCRIPT_DIR%run_ocr.py"