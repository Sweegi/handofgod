$addPath="C:\Program Files (x86)\Tesseract-OCR";
setx path $env:path+';'$addPath;

echo "---- Validate ----"

python --version;
tesseract -v;