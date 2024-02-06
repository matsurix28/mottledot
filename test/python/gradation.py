import cv2
import numpy as np

wid = 255
heig = 255

low = [0,0,0]
up = [180,255,255]

hsv = np.zeros((heig, wid, 3), np.uint8)
h = np.linspace(low[0], up[0], wid)
s = np.linspace(low[1], up[1], wid)
v = np.linspace(low[2], up[2], wid)

for i in range(wid):
    for j in range(heig):
        hsv[j,i,0] = h[i]
        hsv[j,i,1] = s[j]
        hsv[j,i,2] = v[j]

bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imwrite('test.png', bgr)