@echo off
echo ========================================
echo Phase 2 Setup - RAG System Initialization
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed!
    echo.
    echo Please install Docker Desktop for Windows:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    echo After installing Docker, run this script again.
    pause
    exit /b 1
)

echo [1/3] Checking Docker...
docker --version
echo.

echo [2/3] Starting Qdrant vector database...
docker-compose up -d qdrant
echo Waiting for Qdrant to start...
timeout /t 5 /nobreak > nul
echo.

echo [3/3] Initializing documents (this may take 5-30 minutes)...
echo Processing PDFs and generating embeddings...
echo.
cd backend
python scripts/init_documents.py
cd ..
echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo Phase 2 Setup Complete!
    echo ========================================
    echo.
    echo You can now run: start-app.bat
    echo.
) else (
    echo ========================================
    echo Setup Failed!
    echo ========================================
    echo Please check the error messages above.
    echo.
)

pause
