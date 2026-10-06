@echo off
REM Запуск эмулятора (Windows). Параметры передаются дальше.
cd /d "%~dp0"
python src\main.py %*
