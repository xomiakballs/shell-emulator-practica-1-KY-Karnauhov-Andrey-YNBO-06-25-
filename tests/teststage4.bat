@echo off
REM Тест Этапа 4: ls, cd, who, wc, tac + ошибки
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsdeep.csv --script tests\startall4.txt
