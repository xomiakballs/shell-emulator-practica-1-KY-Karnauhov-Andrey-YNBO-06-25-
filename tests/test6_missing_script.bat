@echo off
REM Тест 6: несуществующий скрипт (ошибка)
cd /d "%~dp0.."
python src\main.py --script tests\net_takogo_fayla.txt
