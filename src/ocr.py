"""
Author: Sweegi
"""
import logging

import time
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'

def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()

        t = end - start
        logging.debug("%s cost %s second"%(fn.__name__, t))
    return _wrapper

# 二值化
def _binarize(img, threshold):
    # _img = img.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)

    _img = img.point(table, '1')
    return _img

# 识别文字
def recognize_text(img, txt, threshold):
    # 二值化
    _img_l = img.convert('L')
    _img = _binarize(_img_l, threshold)

    text = pytesseract.image_to_string(_img, lang='chi_sim')
    return txt == text.strip()

# 识别底色
def recognize_color(img, rgb="152-179,188-231,95-128"):
    R, G, B = rgb.split(',')
    r1, r2 = (int(_r) for _r in R.split('-'))
    g1, g2 = (int(_g) for _g in G.split('-'))
    b1, b2 = (int(_b) for _b in B.split('-'))
    
    pix = img.load()
    width = img.size[0]
    height = img.size[1]

    flag = False
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            #  green rgb range
            # R 152-179
            # G 188-231
            # B 95-128
            if r1 <= r <= r2 and g1 <= g <= g2 and b1 <= b <= b2:
                flag = True
                break

        if flag: break

    return flag

if __name__ == '__main__':

    start = time.time()
    recognize_text(Image.open('E://handofgod/src/images/pg1.jpg'), '抛竿', 200)
    print(time.time() - start)