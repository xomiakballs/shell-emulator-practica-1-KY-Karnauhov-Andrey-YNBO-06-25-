@echo off
REM Тест 12: VFS с неверными строками (ошибки)
cd /d "%~dp0.."
python src\main.py --vfs tests\vfsbad.csv --script tests\startvfs.txt
