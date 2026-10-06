@echo off
REM Тест 9: VFS из нескольких файлов
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsseveral.csv --script tests\startvfs.txt
