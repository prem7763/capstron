@echo off
echo ======================================================================
echo Launching Multilingual Course Feedback Intelligence Dashboard...
echo ======================================================================
python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1
pause
