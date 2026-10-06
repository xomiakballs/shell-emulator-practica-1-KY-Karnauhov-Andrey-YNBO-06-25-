@echo off
REM Тест 7: неизвестный параметр и параметр без значения (ошибки)
cd /d "%~dp0.."
python src\main.py --foo --vfs
