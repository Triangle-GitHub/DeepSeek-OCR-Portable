@echo off
setlocal EnableDelayedExpansion

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

"%SCRIPT_DIR%env\python.exe" "%SCRIPT_DIR%run_ocr.py"
pause