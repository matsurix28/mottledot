import cv2
import math
import numpy as np

path = './little.png'

img = cv2.imread(path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

_, bin = cv2.threshold(v, 50, 255, cv2.THRESH_BINARY)
cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = list(filter(lambda x: cv2.contourArea(x) > 500, cnts))
elip = cv2.fitEllipse(cnts[0])
black = np.zeros(img.shape[:3], np.uint8)
bb = black.copy()
cv2.ellipse(black, elip, (255,255,255), -1)
cv2.drawContours(bb, cnts, 0, (255,255,255), -1)

bit = cv2.bitwise_and(bb, black, mask=black)
cv2.imwrite('test.png', bit)

menseki = np.sum(bit) / 255 / 3
print(menseki)

h, w = elip[1]

#menseki = cv2.contourArea(cnts[1])
##area = (h / 2) * (w / 2) * math.pi
#print(h, w)
#print(menseki)
#print(area)