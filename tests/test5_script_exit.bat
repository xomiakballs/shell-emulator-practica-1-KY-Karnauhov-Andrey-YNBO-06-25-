@echo off
REM Тест 5: exit внутри скрипта
cd /d "%~dp0.."
python src\main.py --script tests\startexit.txt
