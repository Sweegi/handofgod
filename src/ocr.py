"""
Author: Sweegi
"""
import time
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'

# 识别文字
def recognize_text(img, txt=None):

    text = pytesseract.image_to_string(img, lang='chi_sim')
    text = text.strip()
    print('Img len: %d, text: "%s"' % (len(text), text))

    return text == txt

def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()

        t = end - start
        print("%s cost %s second"%(fn.__name__, t))
    return _wrapper

# 识别底色
# @time_me
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
                print('yes: rgb: ', r, g, b)
                flat = True
                break
        else:
            continue
        break

    return flag

if __name__ == '__main__':

    # img = 'E://handofgod/src/tempBlack.jpg'
    # recognize_text(Image.open(img))

    recognize_color(Image.open('E://handofgod/src/images/tgSmall.jpg'))

    recognize_color(Image.open('E://handofgod/src/images/tg.jpg'))