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
import matplotlib

    
def detect(image1,image2):
    
    diff_image = skimage.img_as_ubyte(np.absolute(skimage.img_as_int(image2) - skimage.img_as_int(image1)))
    
    
    
    plt.imshow(diff_image)
    plt.text(0,0,"diff")
    plt.show()
    
    filterd_image = skimage.filters.median(diff_image,)
    
    plt.imshow(filterd_image)
    plt.text(0,0,"filtered")
    plt.show()
    
  
    thresh_image = skimage.filters.apply_hysteresis_threshold(filterd_image, 254, 30)
    
    image_et_thresh = image2
    for i in range(len(thresh_image)):
        for j in range(len(thresh_image[0])):
            if(thresh_image[i][j][0]):
                image_et_thresh[i][j] = [255,255,255]
        
    return image_et_thresh


if (__name__ == "__main__"):
    image1 = skimage.io.imread("Inkedgandalf-lord-of-the-rings-e1534255368438_LI (2).jpg")
    image2 = skimage.io.imread("gandalf2.jpg")
    

    test = detect(image1,image2)
    
    plt.imshow(test)
    plt.text(0,0,"mouv")
    plt.show()