@echo off
:: Quick Launch Script for Development
:: ===================================
:: This script quickly launches LuminaReader in development mode

echo Starting LuminaReader...
echo.

:: Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
)

:: Run the application
python main.py %*
