import cv2
import numpy as np
import os
from functools import singledispatch

def main():
    pass

class Kensyutsu:
    def __init__(self, input_path: str, output_path=None) -> None:
        self.set_default

    def set_default(self) -> None:
        self.size = 1000
        self.canny_thr1 = 100
        self.canny_thr2 = 200
        self.bin_thr = 100
        self.bin_max = 255
        self.min_area = 100

    def set_param(self,
                  size=1000,
                  canny_thr1=100,
                  canny_thr2=200,
                  bin_thr=100,
                  bin_max=255,
                  min_area=100
                  )-> None:
        self.size = size
        self.canny_thr1 = canny_thr1
        self.canny_thr2 = canny_thr2
        self.bin_thr = bin_thr
        self.bin_max = bin_max
        self.min_area = min_area

    def detect(self,
               input_path: str, 
               output_path=None, 
               resize=False, 
               save_files=[]
               ) -> None:
        # Set Input and Outpu
        img = cv2.imread(input_path)
        self.img_name = os.path.splitext(os.path.basename(input_path))[0]
        if output_path is None:
            self.output_path = "./"
        else:
            self.output_path = output_path + "/"
        self.save_files = save_files
        
        # Get size
        if resize:
            img = self.resize(img)
        self.height, self.width = img.shape[:2]
        

        # Detection
        hsv_list = self.best_hsv(img)


    def save(self, img: np.ndarray, name: str, ext=".png") -> None:
        output = self.output_path + self.img_name + "_" + name + ext
        cv2.imwrite(output, img)

    def resize(self, img: np.ndarray, name: str = None, ext=".png"
               ) -> np.ndarray:
        scale = self.size / img.shape[1]
        img_resized = cv2.resize(img, dsize=None, fx=scale, fy=scale)
        if "resize" in self.save_files:
            if name is not None:
                tag = "-"
            else:
                tag = ""
            self.save(img_resized, name + tag + "resized", ext=ext)
        return img_resized
    
    def split_hsv(self, img: np.ndarray, name: str = None, ext=".png"
                  ) -> tuple[np.ndarray, ...]:
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_h, img_s, img_v = cv2.split(img_hsv)
        if "hsv" in self.save_files:
            if name is not None:
                tag = "-"
            else:
                tag = ""
            self.save(img_h, name + tag + "h")
            self.save(img_s, name + tag + "s")
            self.save(img_v, name + tag + "v")
        return img_h, img_s, img_v

    def canny(self, img: np.ndarray, name: str = None, ext=".png"
              ) -> np.ndarray:
        img_canny = cv2.Canny(img, self.canny_thr1, self.canny_thr2)
        if "canny" in self.save_files:
            if name is not None:
                tag = "-canny"
            else:
                tag = "canny"
            self.save(img_canny, name + tag, ext=ext)
        return img_canny
    
    def bin(self, img: np.ndarray, name: str = None, ext=".png") -> np.ndarray:
        _, img_bin = cv2.threshold(img, self.bin_thr, self.bin_max, cv2.THRESH_BINARY)
        if "bin" in self.save_files:
            if name is not None:
                tag = "-bin"
            else:
                tag = "bin"
            self.save(img_bin, name + tag, ext=ext)
        return img_bin
    
    def best_hsv(self, img: np.ndarray) -> list[float, np.ndarray, str]:
        img_h, img_s, img_v = self.split_hsv(img)
        hsv_list = [[img_h, "h"], [img_s, "s"], [img_v, "v"]]
        px_list = []
        for image in hsv_list:
            img_canny = self.canny(image[0], name=image[1])
            img_bin = self.bin(img_canny, image[1])
            img_or = cv2.bitwise_or(img, img_bin)
            img_masked = self.bin(img_or, image[1] + "-maseked")
            pixel_num = np.size(img)
            pixel_sum = np.sum(img_masked)
            white_px = pixel_sum / 255
            w_ratio = white_px / pixel_num
            px_list.append([w_ratio, img_masked, image[1]])
        px_list.sort(reverse=True, key=lambda x: x[0])
        return px_list
    
    def contours(self, bin: np.ndarray, img: np.ndarray, name: str = None, ext=".png"):
        cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_area = self.height * self.width / self.min_area
        cnts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
        cv2.drawContours(img, cnts_list, -1, (0,0,255), 5)
        if "contours" in self.save_files:
            if name is not None:
                tag = "-cnt"
            else:
                tag = "cnt"
            self.save(img, name + tag)
        return cnts_list
    
    def check_cnts(self, img: np.ndarray, cnts_list: list):
        

if __name__ == '__main__':
    main()