"""
Author: Sweegi
"""

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'

# 识别文字
def recognize_text(img, txt=None):

    text = pytesseract.image_to_string(img, lang='chi_sim')

    print('Img len: %d, text: "%s"' % (len(text), text))

# 识别底色
def recognize_color(img, color):
    return True


if __name__ == '__main__':

    img = 'E://handofgod/src/temp.jpeg'
    recognize_text(Image.open(img))

    img = 'E://handofgod/src/temp1.jpeg'
    recognize_text(Image.open(img))

    img = 'E://handofgod/src/temp0.jpeg'
    recognize_text(Image.open(img))