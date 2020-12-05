#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:40:11 2020

@author: antoine
"""

import skimage
import skimage.io

import numpy as np

import matplotlib.pyplot as plt
import matplotlib

    
def detect(image1,image2):
    
    diff_image = np.absolute(image1 - image2)
    
    filterd_image = skimage.filters.median(diff_image,)
  
    thresh_image = skimage.filters.apply_hysteresis_threshold(filterd_image, 4, 5)
    return thresh_image


if (__name__ == "__main__"):
    image1= skimage.io.imread("gandalf-lord-of-the-rings-e1534255368438.jpg")
    image2 = skimage.io.imread("Inkedgandalf-lord-of-the-rings-e1534255368438_LI (2).jpg")
    
    plt.imshow(image1)
    plt.imshow(image2)
    #test = detect(image1,image2)
    
    #plt.imshow(test)