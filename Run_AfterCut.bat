@echo off
set "PYTHON=C:\Users\Richmindale\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
set "APP_DIR=%~dp0"

"%PYTHON%" "%APP_DIR%AfterCut.py"
if errorlevel 1 pause
