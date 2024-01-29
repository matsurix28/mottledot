import cv2
import numpy as np
import argparse

def main():
    img1, img2 = args()
    result = pick(img1, img2)
    print(result.shape)

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in1')
    parser.add_argument('--in2')
    args = parser.parse_args()
    return args.in1, args.in2

def pick(img1, img2):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    h, w = img1.shape[:2]
    length = h * w
    img1 = img1.reshape(length, 3)
    img2 = img2.reshape(length, 3)
    result = []
    for i in range(length):
        print(i)
        if not ((img1[i].sum() == 765) and (img2[i].sum == 765)):
            result.append([img1[i], img2[i]])
    return result

if __name__ == '__main__':
    main()