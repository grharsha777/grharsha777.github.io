@echo off
echo Starting Harsha Portfolio AI Backend...
start /b python backend/server.py
echo Waiting for server to start...
timeout /t 5 /nobreak > nul
echo Opening Portfolio in browser...
start http://localhost:8000
echo.
echo Application is running! 
echo Keep this window open while using the app.
echo.
pause
