@echo off
:: LuminaReader Build Script
:: =========================
:: This script builds LuminaReader as a standalone Windows executable
::
:: Usage: build.bat [clean]
::   clean - Optional. Removes build directories before building

setlocal EnableDelayedExpansion

echo ========================================
echo    LuminaReader Build Script
echo ========================================
echo.

:: Check for clean option
if "%~1"=="clean" (
    echo Cleaning previous builds...
    if exist "build" rmdir /s /q "build"
    if exist "dist" rmdir /s /q "dist"
    if exist "__pycache__" rmdir /s /q "__pycache__"
    echo Clean complete.
    echo.
)

:: Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)
for /f "tokens=*" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo Found: %PYTHON_VERSION%
echo.

:: Check virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

:: Install/upgrade dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed.
echo.

:: Run PyInstaller
echo Building executable with PyInstaller...
echo This may take a few minutes...
echo.

pyinstaller LuminaReader.spec --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

:: Check if executable was created
if not exist "dist\LuminaReader_V1.0.exe" (
    echo.
    echo [ERROR] Executable not found!
    echo Build may have failed silently.
    pause
    exit /b 1
)

:: Get file size
for %%I in (dist\LuminaReader_V1.0.exe) do set SIZE=%%~zI
set /a SIZE_MB=%SIZE% / 1024 / 1024

echo.
echo ========================================
echo    Build Successful!
echo ========================================
echo.
echo Output: dist\LuminaReader_V1.0.exe
echo Size: %SIZE_MB% MB
echo.
echo You can now:
echo   1. Run: dist\LuminaReader_V1.0.exe
echo   2. Distribute the executable
echo   3. Create an installer (see BUILD.md)
echo.

:: Deactivate virtual environment
call venv\Scripts\deactivate

pause
