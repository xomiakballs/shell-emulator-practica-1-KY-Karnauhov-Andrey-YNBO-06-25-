@echo off
REM Тест 11: файл VFS не найден (ошибка)
cd /d "%~dp0.."
python src\main.py --vfs tests\net_takoy_vfs.csv
