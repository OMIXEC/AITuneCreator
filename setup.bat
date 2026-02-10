@echo off
REM AITuneCreator Setup Script for Windows
REM This script automates the environment setup for development

setlocal enabledelayedexpansion

REM Colors (Windows 10+)
for /F %%A in ('echo prompt $H ^| cmd') do set "BS=%%A"

REM Check Python
echo.
echo ==== Checking Python Installation ====
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Check if venv exists
echo.
echo ==== Setting Up Virtual Environment ====
if exist "venv" (
    echo [!] Virtual environment already exists, skipping creation
) else (
    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate venv
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Upgrade pip
echo.
echo ==== Upgrading pip ====
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [X] Failed to upgrade pip
    pause
    exit /b 1
)
echo [OK] pip upgraded

REM Install dependencies
echo.
echo ==== Installing Dependencies ====
pip install -e . --quiet
if errorlevel 1 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Verify installation
echo.
echo ==== Verifying Installation ====
python -c "
import sys
modules = ['streamlit', 'langchain', 'groq', 'music21']
print('Checking imports...')
missing = []
for module in modules:
    try:
        __import__(module)
        print(f'  [OK] {module}')
    except ImportError:
        print(f'  [X] {module}')
        missing.append(module)

if missing:
    print(f'\nMissing: {chr(44).join(missing)}')
    sys.exit(1)
"
if errorlevel 1 (
    echo [X] Some dependencies are missing
    pause
    exit /b 1
)
echo [OK] All dependencies found

REM Setup environment files
echo.
echo ==== Setting Up Environment Files ====
if not exist ".env.example" (
    echo [X] .env.example not found
    pause
    exit /b 1
)

echo.
echo Which environments do you want to set up?
echo 1. Development (.env.dev)
echo 2. Testing (.env.test)
echo 3. Production (.env.prod)
echo 4. All of the above
echo 5. Skip (I'll do it manually)
echo.

set /p choice="Enter choice [1-5]: "

if "%choice%"=="1" goto setup_dev
if "%choice%"=="2" goto skip_dev
if "%choice%"=="3" goto skip_dev
if "%choice%"=="4" goto setup_dev
if "%choice%"=="5" goto skip_setup
goto invalid_choice

:setup_dev
if not exist ".env.dev" (
    copy .env.example .env.dev >nul
    echo [OK] .env.dev created from .env.example
    echo [!] Please edit .env.dev and add your GROQ_API_KEY
    echo     Get your key from: https://console.groq.com
) else (
    echo [!] .env.dev already exists
)

:skip_dev
if "%choice%"=="1" goto skip_setup
if "%choice%"=="3" goto skip_setup
if "%choice%"=="4" (
    if not exist ".env.test" (
        copy .env.example .env.test >nul
        powershell -Command "(Get-Content .env.test) -replace 'ENVIRONMENT=dev','ENVIRONMENT=test' | Set-Content .env.test"
        powershell -Command "(Get-Content .env.test) -replace 'STREAMLIT_SERVER_PORT=8501','STREAMLIT_SERVER_PORT=8502' | Set-Content .env.test"
        powershell -Command "(Get-Content .env.test) -replace 'LOG_LEVEL=DEBUG','LOG_LEVEL=INFO' | Set-Content .env.test"
        powershell -Command "(Get-Content .env.test) -replace 'ENABLE_CACHING=false','ENABLE_CACHING=true' | Set-Content .env.test"
        echo [OK] .env.test created with test defaults
    ) else (
        echo [!] .env.test already exists
    )

    if not exist ".env.prod" (
        copy .env.example .env.prod >nul
        powershell -Command "(Get-Content .env.prod) -replace 'ENVIRONMENT=dev','ENVIRONMENT=prod' | Set-Content .env.prod"
        powershell -Command "(Get-Content .env.prod) -replace 'LOG_LEVEL=DEBUG','LOG_LEVEL=WARNING' | Set-Content .env.prod"
        powershell -Command "(Get-Content .env.prod) -replace 'ENABLE_CACHING=false','ENABLE_CACHING=true' | Set-Content .env.prod"
        echo [OK] .env.prod created with prod defaults
        echo [!] Configure .env.prod on production server only!
    ) else (
        echo [!] .env.prod already exists
    )
)

:skip_setup
REM Print next steps
echo.
echo ╔════════════════════════════════════════╗
echo ║        Setup Complete!                 ║
echo ╚════════════════════════════════════════╝
echo.
echo Next steps:
echo 1. Edit your .env files with API keys:
echo    .env.dev - Your development Groq API key
echo    .env.test - Test API key (can be dummy)
echo    .env.prod - Configure on production server
echo.
echo 2. Run the application:
echo    set ENV=dev
echo    streamlit run app.py
echo.
echo 3. Visit: http://localhost:8501
echo.
echo For more information, see:
echo   - DEVELOPER_GUIDE.md (Quick reference)
echo   - CLAUDE.md (Detailed technical guide)
echo.
pause
exit /b 0

:invalid_choice
echo [X] Invalid choice
pause
exit /b 1
