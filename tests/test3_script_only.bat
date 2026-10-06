@echo off
REM Тест 3: только --script
cd /d "%~dp0.."
python src\main.py --script tests\start.txt
