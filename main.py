#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:52:34 2020

@author: antoine
"""

import http_detection_pipeline as dp

import send_email

import tkinter as tk
import time

from PIL import Image,ImageTk
import numpy as np

import io


class movement_detector:
    def __init__(self, parent,cooldown=3600):
        self.cooldown = cooldown
        self.parent = parent
        self.panel = tk.Label(self.parent)
        self.panel.pack(side = "top")
        self.pipeline = dp.Pipeline()
        self.queue = self.pipeline.start()
        self.last_alert_time = None
        self.refresh_label()

    def refresh_label(self):
        new_val = self.queue.get()
        self.image = Image.fromarray(new_val.data)
        if(new_val.alert and (self.last_alert_time == None or (time.perf_counter() - self.last_alert_time) > self.cooldown )):
            print('alert!')
            self.last_alert_time = time.perf_counter()
            imgByteArr = io.BytesIO()
            self.image.save(imgByteArr, format='jpeg')
            send_email.mailto(imgByteArr.getvalue())
        self.parent.after(10, self.refresh_label)
        self.imgtk=ImageTk.PhotoImage(image=self.image)
        self.panel.configure(image=self.imgtk)



if __name__ == "__main__":
    def on_closing():
        mouv_detect.pipeline.kill()
        root.destroy()
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mouv_detect = movement_detector(root)
    root.mainloop()