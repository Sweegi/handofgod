"""
Author: Sweegi
"""

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'

# 识别文字
def recognize_text(img, txt=None):

    text = pytesseract.image_to_string(img, lang='chi_sim')

    print('Img len: %d' % len(text))
    print(text)

# 识别底色
def recognize_color(img, color):
    return True


if __name__ == '__main__':

    img_1 = 'E://handofgod/src/images/1.png'
    img_2 = 'E://handofgod/src/images/2.png'
    img_3 = 'E://handofgod/src/images/3.png'
    t1 = 'E://handofgod/src/images/t1.jpg'
    t2 = 'E://handofgod/src/images/t2.jpg'

    recognize_text(t2)