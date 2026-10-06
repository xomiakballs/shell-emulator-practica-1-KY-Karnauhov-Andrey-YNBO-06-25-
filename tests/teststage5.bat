@echo off
REM Тест Этапа 5: chown + сохранение + ошибки
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsdeep.csv --script tests\startall5.txt
