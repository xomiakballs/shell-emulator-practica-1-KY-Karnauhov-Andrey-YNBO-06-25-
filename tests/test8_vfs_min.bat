@echo off
REM Тест 8: минимальная VFS (один файл)
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsmin.csv --script tests\startvfs.txt
