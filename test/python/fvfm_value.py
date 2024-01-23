import cv2
import easyocr
import re
import itertools
import statistics
import math

def main():
    pass

def yomitori(img_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path)
    fvfm_value = []
    for res in result:
        if re.compile("0(\.|,)\d{2}$").match(res[1]):
            pos = (res[0][3][1] - res[0][0][1]) / 2 + res[0][0][1]
            fvfm_value.append([pos, float((res[1].replace(',', '.'))) * 1000])
    if len(fvfm_value) >= 2:
        fvfm_value.sort(key=lambda x: x[0])
        scale = keisan(fvfm_value)
    else:
        print('Yomitori Sippai')

def keisan(fvfm):
    value_list = []
    for pair in itertools.combinations(fvfm, 2):
        v1 = pair[0][1]
        v2 = pair[1][1]
        h1 = pair[0][0]
        h2 = pair[1][0]

        if h2 > h1:
            v_def = v1 - v2
            h_def = h2 - h1
            scale = h_def / v_def
            value_list.append(scale)
    scale = statistics.median(value_list)
    return scale

def get_scale_area(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY)
    

if __name__ == '__main__':
    main()
