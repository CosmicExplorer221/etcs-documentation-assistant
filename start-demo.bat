@echo off
echo ========================================
echo ETCS Documentation Assistant - DEMO MODE
echo ========================================
echo.

echo Starting Demo Backend Server...
start "Demo Backend" cmd /k "python demo_server.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Demo mode servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Close this window to keep servers running
echo Press any key to exit...
pause > nul
