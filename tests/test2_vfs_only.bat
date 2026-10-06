@echo off
REM Тест 2: только --vfs
cd /d "%~dp0.."
python src\main.py --vfs myvfs.csv
