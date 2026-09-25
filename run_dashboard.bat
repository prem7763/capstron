@echo off
title Multilingual Course Feedback Intelligence - Streamlit Dashboard (Port 8501)
cls
color 0a
echo ======================================================================
echo    STARTING STREAMLIT ANALYTICS DASHBOARD
echo ======================================================================
echo.
echo [1/2] Checking environment & closing stale processes on port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do (
    echo Terminating stale process PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/2] Launching Streamlit on http://127.0.0.1:8501 ...
echo.
echo ======================================================================
echo  IMPORTANT: KEEP THIS COMMAND PROMPT WINDOW OPEN!
echo  Closing this window will stop the dashboard and cause connection errors.
echo ======================================================================
echo.

python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1

echo.
echo Dashboard has stopped.
pause
