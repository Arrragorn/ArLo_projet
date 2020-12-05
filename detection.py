#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:40:11 2020

@author: antoine
"""

import skimage
import numpy as np

    
def detect(image1,image2):
    
    diff_image = np.absolute(image1 - image2)
    
    filterd_image = skimage.filters.median(diff_image,)
  
    thresh_image = skimage.filters.apply_hysteresis_threshold(filterd_image, 4, 5)
    return thresh_image


if (__name__ == "__main__"):
    X = np.array([[12,7,3],
    [4 ,5,6],
    [7 ,8,9]])
        
    Y = np.array([[5,8,1],
    [6,7,3],
    [4,5,9]])
    test = detect(X,Y)
    
    