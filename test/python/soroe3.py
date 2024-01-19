import cv2
import numpy as np

img_fvfm = cv2.imread('./6.png')
img_leaf = cv2.imread('./1.png')

def main():
    test()

def test():
    bin = sbin(img_fvfm)
    cnts, fimg = get_cnts(bin)
    angle, center, _ = elip(cnts)
    rotated = rotate(bin, angle, center)
    ftate = max_tate(fimg)

    lbin = green(img_leaf)
    lcnts, limg = get_cnts(lbin)
    langle, lcenter, lr = elip(lcnts)
    lrotated = rotate(lbin, langle, lcenter)
    ltate = max_tate(limg)
    
    scale = ltate / ftate * 1.08
    fresize = cv2.resize(rotated, dsize=None, fx=scale, fy=scale)
    retate = max_tate(fresize)

    recnts, reimg = get_cnts(fresize)
    reangle, recenter, fr = elip(recnts)

    lcut = kiru(lrotated, lr)
    fcut = kiru(reimg, lr)

    cv2.imwrite('test.png', lrotated) 

def green(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(img_hsv, (30,50,50), (90,255,255))
    return green

def sbin(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    _, bin = cv2.threshold(s, 10, 255, cv2.THRESH_BINARY)
    return bin

def get_cnts(img):
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bets_cnts = max(cnts, key=lambda x: cv2.contourArea(x))
    black = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(black, [bets_cnts], 0, 255, -1)
    return bets_cnts, black

def elip(cnts):
    ellipse = cv2.fitEllipse(cnts)
    angle = ellipse[2]
    center = ellipse[0]
    rudius = ellipse[1]
    return angle, center, rudius

def rotate(img, angle, center):
    h, w = img.shape[:2]
    corners = np.array([(0,0), (w,0), (w,h), (0,h)])
    radius = np.sqrt(max(np.sum((center - corners)**2, axis=1)))
    frame = int(2 * radius)
    trans = cv2.getRotationMatrix2D(center, angle - 90, 1)
    trans[0][2] += radius - center[0]
    trans[1][2] += radius - center[1]
    rotated = cv2.warpAffine(img, trans, (frame, frame))
    return rotated

def max_tate(bin):
    tate = (bin == 255).sum(axis=0)
    maxtate = tate.max()
    return maxtate

def kiru(img, haba, prm=0):
    h, w = img.shape[:2]
    t, y = haba[:2]
    cut = img[int(h/2 - t) : int(h/2 + t), int(w/2 - y - prm) : int(w/2 + y - prm)]
    return cut

if __name__ == '__main__':
    main()