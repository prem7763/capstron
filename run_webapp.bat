@echo off
title Multilingual Course Feedback Intelligence - Web Server (Port 8000)
cls
color 0b
echo ======================================================================
echo    STARTING MULTILINGUAL COURSE FEEDBACK INTELLIGENCE
echo ======================================================================
echo.
echo [1/3] Checking environment & closing stale processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Terminating stale process PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/3] Initializing NLP Pipeline & FastAPI Backend...
echo [3/3] Your browser will open automatically once the server is ready!
echo.
echo ======================================================================
echo  IMPORTANT: KEEP THIS COMMAND PROMPT WINDOW OPEN!
echo  Closing this window will stop the server and cause connection errors.
echo  To shut down the server safely, press CTRL+C in this window.
echo ======================================================================
echo.

python server.py

echo.
echo Server has stopped.
pause
