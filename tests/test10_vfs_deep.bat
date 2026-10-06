@echo off
REM Тест 10: VFS с 3 уровнями папок и base64-файлом
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsdeep.csv --script tests\startvfs.txt
