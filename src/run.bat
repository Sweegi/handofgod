@echo off
chcp 936

python --version
tesseract -v

echo "---- start ----"

python main.py
pause