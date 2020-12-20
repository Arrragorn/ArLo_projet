#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:15:16 2020

@author: antoine
"""

import requests
from PIL import Image
from io import BytesIO

import numpy as np 




def get_image(pic_url='http://205.237.248.39/axis-cgi/jpg/image.cgi?resolution=640x480'):
    response = requests.get(pic_url)
    return np.array(Image.open(BytesIO(response.content)))

    
#tests pour ce module
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import time
    
    
    #pic_url = 'http://205.237.248.39/axis-cgi/jpg/image.cgi?resolution=640x480'
    n=20
    
    
    time_start = time.perf_counter()
    for i in range(n):
        img = get_image()
        #plt.imshow(img)
        #plt.show()
    time_end = time.perf_counter()
    time_total = time_end-time_start
    time_per_it = time_total/n
    
    print('temps par images: '  + str(time_per_it))