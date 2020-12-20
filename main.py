#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:52:34 2020

@author: antoine
"""


import flux_images
import detection

import tkinter as tk
import time

from PIL import Image,ImageTk
import numpy as np


class movement_detector:
    def __init__(self, parent):
        #self.img =  ImageTk.PhotoImage(image=Image.fromarray(array))
        self.parent = parent
        self.panel = tk.Label(self.parent)
        self.panel.pack(side = "top")
        self.detector = detection.detector()
        self.refresh_label()

    def refresh_label(self):
        self.parent.after(1000, self.refresh_label)
        t_start= time.perf_counter()
        self.array = flux_images.get_image()
        t_get = time.perf_counter()
        self.img = Image.fromarray( self.detector.detect(self.array))
        t_detect = time.perf_counter()
        self.imgtk=ImageTk.PhotoImage(image=self.img)
        self.panel.configure(image=self.imgtk)
        t_display = time.perf_counter()
        print('get: ' + str(t_get-t_start) )
        print('detect: ' + str(t_detect-t_get))
        print('show: ' + str(t_display-t_detect) )

if __name__ == "__main__":
    root = tk.Tk()
    timer = movement_detector(root)
    root.mainloop()