import cv2
import numpy as np
import os

def main():
    pass

class Kensyutsu:
    def __init__(self):
        self.set_default()

    def set_default(self) -> None:
        self.resize = 1000
        self.canny_thr1 = 100
        self.canny_thr2 = 200
        self.bin_thr = 100
        self.bin_max = 255
        self.min_area = 100
        self.hsv_min = np.array([30,50,50])
        self.hsv_max = np.array([90,255,200])

    def set_param(self,
                  resize=1000,
                  canny_thr1=100,
                  canny_thr2=200,
                  bin_thr=100,
                  bin_max=255,
                  min_area=100,
                  hsv_min=[30,50,50],
                  hsv_max=[90,255,200]
                  ) -> None:
        self.resize = resize
        self.canny_thr1 = canny_thr1
        self.canny_thr2 = canny_thr2
        self.bin_thr = bin_thr
        self.bin_max = bin_max
        self.min_area = min_area
        self.hsv_min = np.array(hsv_min)
        self.hsv_max = np.array(hsv_max)

    def save(self, img: np.ndarray, name: str, ext='.png') -> None:
        """Save as image file.
        
        Args:
            img (np.ndarray): input image
            name (str): file name without extension
            ext (str): extension
        """
        output = self.output_path + self.img_name + '_' + name + ext
        cv2.imwrite(output, img)

    def resize(self, img: np.ndarray, name: str = '', ext='.png') -> np.ndarray:
        scale = self.resize / img.shape[1]
        img_resized = cv2.resize(img, None, fx=scale, fy=scale)
        if 'resize' in self.save_files:
            if name == '':
                tag = '-'
            else:
                tag = ''
            self.save(img_resized, name + tag + 'resized', ext=ext)
        return img_resized
    
    def split_hsv(self, img: np.ndarray, name: str = '', )

if __name__ == '__main__':
    main()