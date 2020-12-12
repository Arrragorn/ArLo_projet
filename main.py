#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:52:34 2020

@author: antoine
"""


import flux_images
import detection

import tkinter as tk

from PIL import Image,ImageTk
import numpy as np


class movement_detector:
    def __init__(self, parent):
        #self.img =  ImageTk.PhotoImage(image=Image.fromarray(array))
        self.parent = parent
        self.panel = tk.Label(self.parent)
        self.panel.pack(side = "top")
        self.refresh_label()

    def refresh_label(self):
        self.parent.after(1000, self.refresh_label)
        self.old_array = self.new_array 
        self.img = Image.fromarray(  flux_images.get_image())
        self.imgtk=ImageTk.PhotoImage(image=self.img)
        self.panel.configure(image=self.imgtk)
        

if __name__ == "__main__":
    root = tk.Tk()
    timer = movement_detector(root)
    root.mainloop()