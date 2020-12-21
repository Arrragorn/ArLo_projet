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

import time 

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
        
        
@jit(nopython=True)
def quick_median(img_8_bit):
    histogram = np.zeros(256)
    dim = img_8_bit.shape
    l_dim = dim[0]
    c_dim = dim[1]
    for i in range(l_dim):
        for j in range(c_dim):
            index = img_8_bit[i][j]
            histogram[index]=histogram[index]+1
    median_pos = np.ceil((l_dim*c_dim)/2)
    actual_pos = 0
    median_value=0
    is_found = False
    for i in range(256):
        actual_pos+=histogram[i]
        if(not is_found and actual_pos>=median_pos):
            median_value = i
            is_found = True
    return median_value
        
@jit(nopython=True)
def rgb_to_wb(img):
    dim = img.shape
    l_dim = dim[0]
    c_dim = dim[1]
    
    wb_img = np.empty((l_dim,c_dim))
    for i in range(l_dim):
        for j in range(c_dim):
            wb_img[i][j] = (img[i][j][0] + img[i][j][1] + img[i][j][2])/3
    return wb_img


@jit(nopython=True)
def median_filter(img,l_half_window,c_half_window):
    dim = img.shape
    l_dim = dim[0]
    c_dim = dim[1]
    filtered_img = np.zeros((l_dim,c_dim))
    for i in range(l_half_window,l_dim -l_half_window):
        for j in range(c_half_window,c_dim -c_half_window):
            filtered_img[i][j] = \
            quick_median(img[i-l_half_window:i+l_half_window+1,
                          j-c_half_window:j+c_half_window+1])
    return filtered_img

@jit(nopython=True)
def tresh(img,high):
    return img > high

@jit(nopython=True)
def contour_bool(img_bool):
    dim = img_bool.shape
    l_dim = dim[0]
    c_dim = dim[1]
    contour_img = np.empty((l_dim,c_dim))
    for i in range(1,l_dim - 1):
        for j in range(1,c_dim - 1):
 
            if not img_bool[i][j]:
                contour_img[i][j] = img_bool[i-1][j-1] or img_bool[i-1][j+1] or \
                img_bool[i+1][j-1] or img_bool[i+1][j+1]
            else:
                contour_img[i][j] = False
    return contour_img
    


@jit(nopython=True)
def diff_of_images(img_wb_1,img_wb_2):
    return np.absolute( img_wb_2 - img_wb_1 )



    

@jit(nopython=True)
def display_contour(img,contour):
    image_et_contour = img.copy()
    for i in range(len(image_et_contour)):
        for j in range(len(image_et_contour[0])):
            if(contour[i][j]):
                image_et_contour[i][j] = [0,255,0]
    return image_et_contour

def detect(image1,image2):
    
    t_start = time.perf_counter()
    
    
    img_wb_1 = rgb_to_wb(image1)
    img_wb_2 = rgb_to_wb(image2)
    
    t_wb = time.perf_counter()
    print('wb: ' + str(t_wb-t_start))

    
    diff_image = diff_of_images(img_wb_1,img_wb_2).astype(np.uint8)
    
    t_diff = time.perf_counter() 
    print('diff: ' + str(t_diff-t_wb))
    
    
    #plt.imshow(diff_image)
    #plt.text(0,0,"diff")
    #plt.show()
    
    #avec 4 et 4 excellent resultats mais 420ms...
    filterd_image = median_filter(diff_image,4, 4)
    
    t_filt = time.perf_counter() 
    print('filt: ' + str(t_filt-t_diff))
    
    #plt.imshow(filterd_image)
    #plt.text(0,0,"filtered")
    #plt.show()
    
    
    thresh_image = tresh(filterd_image,40)
    
    t_tresh = time.perf_counter() 
    print('tresh: ' + str(t_tresh-t_filt))
    
    contour_image = contour_bool(thresh_image)
    
    t_cont = time.perf_counter() 
    print('cont: ' + str(t_cont-t_tresh))
    
    contour_et_image = display_contour(image2,contour_image)
    
    t_disp = time.perf_counter() 
    print('disp: ' + str(t_disp-t_cont))
    
    return contour_et_image

#tests pour ce module
if (__name__ == "__main__"):
    image1 = skimage.io.imread("Inkedgandalf-lord-of-the-rings-e1534255368438_LI (2).jpg")
    image2 = skimage.io.imread("gandalf2.jpg")
    
    num = 20 
    test = detect(image1, image2)
    
    t_start= time.perf_counter()
    
    
    for i in range(num):
        test = detect(image2, image1)
    t_stop = time.perf_counter()
    t_total = t_stop-t_start
    print(t_total/num)
    
    plt.imshow(test)
    plt.text(0,0,"mouv")
    plt.show()