#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 22:32:43 2020

@author: antoine
"""

import detection
import flux_images
import numpy as np
import time
    
import matplotlib.pyplot as plt

from multiprocessing import Process,Queue



def stage_reception(q_in,q_out):
    while(True):
        t_start = time.perf_counter() 
        if(not q_in.empty()):
            if q_in.get().kill:
                return
        q_out.put(PipeData(flux_images.get_image()))
        print('reception: ' + str(time.perf_counter() - t_start))

        
def stage_filter(q_in,q_out,window_half_size):
    while(True):
        to_process = q_in.get()
        if to_process.kill:
                return
        q_out.put(detection.median_filter(to_process.data,window_half_size,window_half_size))
    
def stage_main(q_in,q_out,num_process,window_half_size,tresh_limit):
    old_image=[]
    new_image=[]
    while(True):
        old_image = new_image
        new_val = q_in.get()
        t_start = time.perf_counter()
        if new_val.kill:
                return
        new_image_rgb = new_val.data
        new_image = detection.rgb_to_wb(new_image_rgb)
        if(len(old_image)!=0):
            diff_of_images = detection.diff_of_images(old_image,new_image).astype(np.uint8)
            #num_ligne = diff_of_images.shape[0]
            #for i in range(num_process):
            #   inf_limit = int(min(np.round(i*num_ligne/num_process - window_half_size),0))
            #   sup_limit = int( max(np.round(num_ligne*((i+1)/num_process) + window_half_size),num_ligne))
            #    qs_in_filter[i].put(PipeData( diff_of_images[inf_limit:sup_limit]))
                
            #filtered_image = qs_out_filter[0].get()[window_half_size+1:]
            #for i in range(1,num_process-1):
            #    filtered_image = np.append(filtered_image,
            #                               qs_out_filter[i].get()[window_half_size+1:-window_half_size],axis=0)
            #filtered_image = np.append(filtered_image,
            #                           qs_out_filter[num_process-1].get()[:-window_half_size],axis=0) 
            filtered_image = detection.median_filter(diff_of_images,window_half_size,window_half_size)
            tresh_image = detection.tresh(filtered_image,tresh_limit)
            contour_image = detection.contour_bool(tresh_image)
            alert = tresh_image.any()
            contour_et_image  = detection.display_contour(new_image_rgb,contour_image)
            q_out.put(PipeData(contour_et_image,alert=alert))
        else:
            q_out.put(PipeData(new_image_rgb))
        print('detection: ' + str(time.perf_counter() - t_start))
            
class PipeData:
    def __init__(self,data=[],kill=False,alert=False):
        self.alert=alert
        self.data = data
        self.kill = kill
    
            
class Pipeline:
    def __init__(self,num_process_filter=3,window_half_size=4,tresh_level=40):
        self.num_process_filter  = num_process_filter
        self.queue_pour_detection = Queue()
        self.queue_pour_affichage = Queue()
        self.queue_pour_reception = Queue()
        #self.queue_de_filtre = []
        #self.queue_pour_filtre = []
        #for i in range(num_process_filter):
        #    self.queue_de_filtre.append(Queue())
         #   self.queue_pour_filtre.append(Queue())
            
        self.stage_reception = Process(target=stage_reception, args=(self.queue_pour_reception,self.queue_pour_detection,))
        self.stage_main = Process(target=stage_main, args=(self.queue_pour_detection,
                                                           self.queue_pour_affichage,
                                                           #self.queue_pour_filtre,
                                                           #self.queue_de_filtre,
                                                           num_process_filter,
                                                           window_half_size,
                                                           tresh_level,))
        #self.stages_filter = []
        #for i in range(num_process_filter):
         #   self.stages_filter.append(Process(target=stage_filter, args=(self.queue_pour_filtre[i],
        #                                                   self.queue_de_filtre[i],
         #                                                  window_half_size,)))
        
    def start(self):
        self.stage_reception.start()
        #for i in range(self.num_process_filter):
        #    self.stages_filter[i].start()
        self.stage_main.start()
        return self.queue_pour_affichage
    def kill(self):
        
        self.queue_pour_detection.put(PipeData(kill=True))
        #for i in range(self.num_process_filter):
        #    self.queue_pour_filtre[i].put(PipeData(kill=True))
            
        self.queue_pour_reception.put(PipeData(kill=True))
        
        
        
if __name__=='__main__':
    num = 20 
    
    test = Pipeline()
    queu_test = test.start()
    
    t_start= time.perf_counter()
    for i in range(num):
        plt.imshow(queu_test.get().data)
        plt.text(0,0,"test")
        plt.show()
        
    t_stop = time.perf_counter()
    t_total = t_stop-t_start
    print(t_total/num)
    test.kill()
    