@echo off
title Multilingual Course Feedback Intelligence - Web Application
echo ======================================================================
echo    STARTING MULTILINGUAL COURSE FEEDBACK INTELLIGENCE (FASTAPI)
echo ======================================================================
echo.
echo Launching backend server on http://127.0.0.1:8000 ...
echo.

start "" http://127.0.0.1:8000
python server.py

pause
