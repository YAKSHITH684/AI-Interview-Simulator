@echo off

cd /d "C:\Users\nxt68\OneDrive\ドキュメント\PROJECTS AIML\AI Interview Simulator\Backend"

if errorlevel 1 (
    echo ERROR: Backend folder not found!
    pause
    exit /b
)

echo Starting Backend...
start "" python -m uvicorn app:app --reload

timeout /t 6 >nul

echo Opening browser...
start "" http://127.0.0.1:8000/docs

pause