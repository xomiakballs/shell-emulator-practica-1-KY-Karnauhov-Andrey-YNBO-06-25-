@echo off
REM Тест Этапа 3: все команды + VFS + ошибки
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsdeep.csv --script tests\startall3.txt
