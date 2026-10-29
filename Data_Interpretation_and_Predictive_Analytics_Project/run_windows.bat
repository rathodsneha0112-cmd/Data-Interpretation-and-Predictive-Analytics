@echo off
setlocal
cd /d "%~dp0"
title DATA INTERPRETATION AND PREDICTIVE ANALYTICS

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating project virtual environment...
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        where python >nul 2>nul
        if errorlevel 1 (
            echo ERROR: Python was not found. Install Python 3.11+ and enable Add Python to PATH.
            pause
            exit /b 1
        )
        python -m venv .venv
    )
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo [2/3] Checking required packages...
".venv\Scripts\python.exe" -c "import streamlit, matplotlib, numpy" >nul 2>nul
if errorlevel 1 (
    echo Installing required packages. Internet access is needed for first-time setup.
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Package installation failed. Check internet access, then try again.
        pause
        exit /b 1
    )
) else (
    echo Required packages are already installed.
)

echo [3/3] Starting website...
".venv\Scripts\python.exe" -m streamlit run streamlit_app.py
if errorlevel 1 (
    echo The website stopped with an error. Check the message above.
    pause
    exit /b 1
)
endlocal
