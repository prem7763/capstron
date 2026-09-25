@echo off
title Multilingual Course Feedback Intelligence - Master Launcher
cls
color 0e
echo ======================================================================
echo    MULTILINGUAL COURSE FEEDBACK INTELLIGENCE - MASTER LAUNCHER
echo ======================================================================
echo.
echo Please select which application you would like to run:
echo.
echo   [1] Modern Full-Stack Web Application (Recommended - Port 8000)
echo       - Interactive CRUD (Add/Delete feedback)
echo       - Live Multilingual NLP Sandbox Playground
echo       - Dark Glassmorphism & Chart.js Visuals
echo.
echo   [2] Streamlit Analytics Dashboard (Port 8501)
echo       - Classical Data Science Multi-filter View
echo       - Deep Statistical Distribution Plots
echo.
echo   [3] Launch BOTH Applications Simultaneously
echo.
echo ======================================================================
set /p choice="Enter choice (1, 2, or 3) [Default: 1]: "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    echo.
    echo Starting Modern Web Application...
    start "Web App (Port 8000)" run_webapp.bat
    exit
)

if "%choice%"=="2" (
    echo.
    echo Starting Streamlit Dashboard...
    start "Streamlit (Port 8501)" run_dashboard.bat
    exit
)

if "%choice%"=="3" (
    echo.
    echo Starting Both Web App and Streamlit Dashboard...
    start "Web App (Port 8000)" run_webapp.bat
    start "Streamlit (Port 8501)" run_dashboard.bat
    exit
)

echo Invalid choice. Starting Modern Web Application by default...
start "Web App (Port 8000)" run_webapp.bat
exit
