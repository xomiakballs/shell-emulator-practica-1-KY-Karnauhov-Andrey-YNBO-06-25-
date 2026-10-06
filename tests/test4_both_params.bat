@echo off
REM Тест 4: оба параметра
cd /d "%~dp0.."
python src\main.py --vfs myvfs.csv --script tests\start.txt
