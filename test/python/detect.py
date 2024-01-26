#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""Detect and extract leaves and fvfm scale bar."""

import cv2
import numpy as np
import os
import sys

def main():
    d = Detect()
    #d.test('naname.JPG')
    try:
        d.extr_green_leaves('mottle.JPG')
    except (TypeError, ValueError) as e:
        print(e)
        sys.exit()

class Detect:
    """Detect and extract leaves and fvfm scale bar.
    
    Extract fresh leaves, stained leaves, Fv/Fm value scale bar 
    from an image, and detect each leaf size and tilt.
    
    Attributes:
        resize (:obj:`int`): Image size after resizing. Defaults to 1000.
        canny_thr1 (:obj:`int`): Canny threshold1. Defaults to 100.
        canny_thr2 (:obj:`int`): Canny threshold2. Defaults to 200.
        bin_thr (:obj:`float`): Threshold of binarization. Defaults to 60.
        bin_max (:obj:`float`): Max value of binarization. Defaults to 255.
        min_area (:obj:`int`): Minimun leaf area as a fraction of the 
            image. Defaults to 100.
        hsv_min (:obj:`numpy.ndarray[int]`): Minimum HSV value of green.
            Defaults to [30, 50, 50].
        hsv_max (:obj:`numpy.ndarray[int]`): Maximum HSV value of green. 
            Defaults to [90, 255, 200].
        blur (:obj:`tuple`): Kernel size of blur (width, height). 
            Defaults to (5,5)
        output_path (:obj:`str`): Output path. Defaults to './'
    """

    def __init__(self) -> None:
        self.__set_default()

    def __set_default(self) -> None:
        """Set default value to each parameter."""
        self.__resize = 1000
        self.canny_thr1 = 100
        self.canny_thr2 = 200
        self.bin_thr = 50
        self.bin_max = 255
        self.min_area = 100
        self.hsv_min = np.array([30,50,50])
        self.hsv_max = np.array([90,255,200])
        self.blur = (5,5)
        self.output_path = './'

    def set_param(self,
                  resize=1000,
                  canny_thr1=100,
                  canny_thr2=200,
                  bin_thr=60,
                  bin_max=255,
                  min_area=100,
                  hsv_min=[30,50,50],
                  hsv_max=[90,255,200],
                  blur=(5,5),
                  output_path='./'
                  ) -> None:
        """Set value to each parameter.
        
        Args:
            resize (:obj:`int`, optional): Image size after resizing. 
                Defaults to 1000.
            canny_thr1 (:obj:`int`, optional): Canny threshold1. 
                Defaults to 100.
            canny_thr2 (:obj:`int`, optional): Canny threshold2. 
                Defaults to 200.
            bin_thr (:obj:`float`, optional): Threshold of binarization. 
                Defaults to 60.
            bin_max (:obj:`float`, optional): Max value of binarization. 
                Defaults to 255.
            min_area (:obj:`int`, optional): Minimun leaf area 
                as a fraction of the image. Defaults to 100.
            hsv_min (:obj:`list[int]`, optional): Minimum HSV value of 
                green. Defaults to [30, 50, 50].
            hsv_max (:obj:`list[int]`, optional): Maximum HSV value of 
                green. Defaults to [90, 255, 200].
            blur (:obj:`tuple`): Kernel size of blur (width, height).
                Defaults to (5,5).
            output_path (:obj:`str`): Output path. Default to './'

        Returns:
            None
        """
        self.__resize = resize
        self.canny_thr1 = canny_thr1
        self.canny_thr2 = canny_thr2
        self.bin_thr = bin_thr
        self.bin_max = bin_max
        self.min_area = min_area
        self.hsv_min = np.array(hsv_min)
        self.hsv_max = np.array(hsv_max)
        self.blur = blur
        self.output_path = output_path

    def __save(self, img: np.ndarray, name: str, ext='.png') -> None:
        """Save as image file.
        
        Args:
            img (:obj:`numpy.ndarray`): Image to save
            name (:obj:`str`): File name without extension
            ext (:obj:`str`, optional): File extension. 
                Defaults to '.png'
        
        Returns:
            None
        """
        output = self.output_path + self.img_name + '_' + name + ext
        cv2.imwrite(output, img)

    def __resize(self, img: np.ndarray) -> np.ndarray:
        """Resize image.
        
        Args:
            img (:obj:`numpy.ndarray`): Input image.

        Returns:
            numpy.ndarray: Resized image.
        """
        scale = self.__resize / img.shape[1]
        img_resized = cv2.resize(img, None, fx=scale, fy=scale)
        return img_resized

    def __get_cnts(self, img: np.ndarray) -> list:
        """Find contours with an area larger than the set value.
        
        Args:
            img (:obj:`numpy.ndarray`): Input binary image.

        Returns:
            list: Contours with an area larger than the set value.
        """
        cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)
        height, width = img.shape[:2]
        min_area = height * width / self.min_area
        cnts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
        return cnts_list
    
    def __assess_noise(self, img: np.ndarray) -> int:
        """Assess noise of image.
        
        Args:
            img (:obj:`numpy.ndarray`): Input image.

        Returns:
            int: Number of noise.
        """
        img_canny = cv2.Canny(img, self.canny_thr1, self.canny_thr2)
        cnts, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        height, width = img.shape[:2]
        min_area = height * width / 1000
        cnts_list = list(filter(lambda x: cv2.contourArea(x) < min_area, cnts))
        return len(cnts_list)

    def __bin(self, img: np.ndarray) -> np.ndarray:
        """Binarization.
        
        Args:
            img (:obj:`numpy.ndarray`): Input gray scale image.

        Returns:
            numpy.ndarray: Binary image.
        """
        _, img_bin = cv2.threshold(img, self.bin_thr, self.bin_max, 
                                   cv2.THRESH_BINARY)
        return img_bin

    def __green_range(self, img: np.ndarray) -> np.ndarray:
        """Extract green region.
        
        Args:
            img (:obj:`numpy.ndarray`): Input color image.

        Returns:
            numpy.ndarray: Image of green only.
        """
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_hsv = cv2.inRange(img_hsv, self.hsv_min, self.hsv_max)
        return mask_hsv
    
    def test(self, input_path):
        img = cv2.imread(input_path)
        img = cv2.blur(img, (5,5))
        cnts_list = self.__best_hsv(img)
        #cv2.drawContours(img, [cnts_list[0][1]], 0, (0,0,255), -1)
        #cv2.imwrite('test.png', img)
        green = self.__green_ratio(img, cnts_list[0][1])
        print(green)

    def extr_green_leaves(self, input_path: str, output_path: str = './') -> np.ndarray:
        try:
            img = self.__input_img(input_path)
        except (TypeError, ValueError) as e:
            raise
        cnts_list = self.__best_hsv(img)
        main_obj = self.__main_obj(img, cnts_list[0])
        cv2.drawContours(img, [main_obj], 0, (0,0,255), -1)
        cv2.imwrite('tst.png', img)

    def __input_img(self, path: str) -> np.ndarray:
        if os.path.isfile(path):
            img = cv2.imread(path)
            if not isinstance(img, np.ndarray):
                raise TypeError(f'\'{path}\' is not an image file')
            else:
                return img
        else:
            raise ValueError(f'Cannot access \'{path}\': No such file or directory')

    def __leaf_shape(self):
        pass        

    def __main_obj(self, img: np.ndarray, cnts: np.ndarray) -> np.ndarray:
        h, w = img.shape[:2]
        center = (int(w /2), int(h / 2))
        main_obj = None
        obj_list = []
        for cnt in cnts:
            dist = cv2.pointPolygonTest(cnt, center, True)
            obj_list.append([dist, cnt]) 
            if dist >= 0:
                main_obj = cnt
        if main_obj is None:
            obj_list.sort(key=lambda x: x[0], reverse=True)
            main_obj = obj_list[0][1]
        return main_obj


    def __green_ratio(self, img: np.ndarray, cnts: np.ndarray) -> float:
        h, w = img.shape[:2]
        mask = np.zeros((h, w, 3), np.uint8)
        cv2.drawContours(mask, [cnts], 0, (255, 255, 255), -1)
        masked = cv2.bitwise_and(img, mask)
        green = self.__green_range(masked)
        mask_area = np.sum(mask) / 255 /3
        green_area = np.sum(green) / 255
        green_ratio = green_area / mask_area
        print('gren area: ',green_area)
        print('mask area: ', mask_area)
        a = h* w
        print('total area: ', a)
        return green_ratio


    def __best_hsv(self, img: np.ndarray) -> list:
        """Sort H, S, and V in order of decreasing noise
        
        Args:
            img (:obj:`numpy.ndarray`): Input color image.

        Returns:
            list: List of contours sorted in order of decreasing noise. 
        """
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv = cv2.split(img_hsv)
        best = []
        h, w = img.shape[:2]
        area = h * w
        for image in hsv:
            bin = self.__bin(image)
            white = np.sum(bin) / 255
            black = area - white
            if (white / area) > 0.98 or (black / area) > 0.98:
                continue
            cnts = self.__get_cnts(bin)
            noise = self.__assess_noise(image)
            if len(cnts) > 0:
                best.append([noise, cnts])
        best.sort(key=lambda x: x[0])
        result = [r[1] for r in best]
        return result


if __name__ == '__main__':
    main()