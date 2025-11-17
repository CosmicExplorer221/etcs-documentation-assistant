@echo off
echo ========================================
echo ETCS Documentation Assistant - Startup
echo ========================================
echo.

echo Starting Backend Server...
start "Backend API" cmd /k "cd backend && python -m app.main"

timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Close this window to keep servers running
echo Press any key to exit...
pause > nul
