import easyocr
import cv2
import re

out_path = "test/output/ocr/"

def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

reader = easyocr.Reader(['en'])
path = "test/img/bar.bmp"

#img = cv2.imread(path)
#img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#_, img_bin = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
#save("bin.bmp", img_bin)

ppath = out_path + "bin.bmp"
result = reader.readtext(path)
#result = [["aaa", "0.5"], ["bbbb", "1.7"], ["dddd", "0.89"]]
print([row[1] for row in result])

fvfm_scale = []
for res in result:
    if re.compile("0(\.|,)\d{2}$").match(res[1]): 
        pos = (res[0][3][1] - res[0][0][1]) / 2 + res[0][0][1]
        fvfm_scale.append([pos, res[1].replace(',', '.')])

if len(fvfm_scale) >= 2:
    print("keisan suruyo")

else:
    print("taran")

print(fvfm_scale)


#img = cv2.imread(path)
#img_1 = img.copy()

#for i in range(len(res)):
#    cv2.rectangle(img_1, res[i][0][0], res[i][0][2], (0,255,0), 3)

#save("basho.jpeg", img_1)