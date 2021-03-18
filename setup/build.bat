@echo off
chcp 936
setx TESSDATA_PREFIX "C:\Program Files (x86)\Tesseract-OCR"
setx "path" "%path%;C:\Program Files (x86)\Tesseract-OCR;"
pip3 install -r packages.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

echo "---- End ----"
pause