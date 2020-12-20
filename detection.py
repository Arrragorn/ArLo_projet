#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:40:11 2020

@author: antoine
"""

import skimage
import skimage.io
import skimage.filters

import numpy as np

import matplotlib.pyplot as plt

from numba import jit


class detector:
    def __init__(self):
        self.img = []
        self.img_old = []
        
    def detect(self,img_new):
        self.img_old = self.img
        self.img = img_new
        if(self.img_old!=[]):
            return detect(self.img_old,self.img)
        else:
            return self.img
            
def rgb_to_wb(img):
    dim = img.shape
    wb_img = np.empty(dim)
    for i in len(img):
        for j in :
            
        
        
def detect(image1,image2):
    1ch_image1 = [  image1]
    diff_image = skimage.img_as_ubyte(np.absolute(skimage.img_as_int(image2) - skimage.img_as_int(image1)))
    filterd_image = skimage.filters.median(diff_image,)
    thresh_image = skimage.filters.apply_hysteresis_threshold(filterd_image, 255, 40)
    image_et_thresh = image2.copy()
    for i in range(len(thresh_image)):
        for j in range(len(thresh_image[0])):
            if(thresh_image[i][j][0]):
                image_et_thresh[i][j] = [255,255,255]
    return image_et_thresh

#tests pour ce module
if (__name__ == "__main__"):
    image1 = skimage.io.imread("Inkedgandalf-lord-of-the-rings-e1534255368438_LI (2).jpg")
    image2 = skimage.io.imread("gandalf2.jpg")
    

    test = detect(image2,image1)
    
    plt.imshow(test)
    plt.text(0,0,"mouv")
    plt.show()