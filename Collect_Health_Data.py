import mss
import mss
import mss.tools
import time
import numpy as np
from PIL import Image
import os
import cv2
from collections import deque

import tensorflow as tf
from tensorflow import keras
import pynput
from pynput.mouse import Listener, Controller
from pynput.keyboard import Key

import win32gui

def callback(hwnd, extra):
    if(win32gui.GetWindowText(hwnd)=="Diablo II"):
        rect = win32gui.GetWindowRect(hwnd)
        
        x = rect[0]
        y = rect[1]+25
        w = rect[2]-(x)
        h = rect[3]-(y)
        
        #print("Window %s:" % win32gui.GetWindowText(hwnd))
        extra[0] = (x, y)
        extra[1] = (w, h)
        #print("\t    Size: (%d, %d)" % (w, h))
        #print("\t    Location: (%d, %d)" % (x, y))


class Custom_Listener(Listener):    
    def __init__(self):
        
        #self.health_model = keras.models.load_model('detect_health.h5')
        #self.mana_model = keras.models.load_model('detect_mana.h5')
        self.inv_model = keras.models.load_model('Pot_Detection.h5')
        
        #model.summary()
        self.mouse = Controller()
        self.control = pynput.keyboard.Controller()
        self.health_column_names = ["full health", "slightly hurt", "hurt", "critically hurt"]
        self.mana_column_names = ["full mana", "good mana", "low mana", "no mana"]
        
        self.itm_labels = [ '', 'misc',
            'minor health','minor mana',
            'light health','light mana',
            'mana', 'health',
            'greater health','greater mana',
            'super health','super mana',
            'rejuv', 'full rejuv'
            ]
        
        self.inv_labels = [
            ["", "", "", "","","","","","",""],
            ["", "", "", "","","","","","",""],
            ["", "", "", "","","","","","",""],
            ["", "", "", "","","","","","",""]
            ]
        
        self.filename = "training_data/training_environment.npy"
        
        
        if os.path.isfile(self.filename):
            print('File exists, loading previous data!')
            self.training_data = list(np.load(self.filename, allow_pickle = True))
        else:
            print('File does not exist, starting fresh!')
            self.training_data = []
        
        

    def collect_ss(self, inv_labels):
        
            #while True:
            screens = [0,0]
            win32gui.EnumWindows(callback, screens)
            
            with mss.mss() as sct:
                    monitor = {"top": screens[0][1], "left":screens[0][0], "width": screens[1][0], "height": screens[1][1]}                
                    sct_img = sct.grab(monitor)
                    
                    sct_img = np.array(sct_img)
                    screen = cv2.cvtColor(sct_img, cv2.IMREAD_GRAYSCALE)
                    screen = self.__adjusted_capture__(screen, 419,317,113,287)
                    #screen = cv2.resize(sct_img, (50,40))
                    print(len(self.training_data))
                    #screen = screen[317:432, 421:713, :]
                    screen = cv2.resize(screen,(300,120))
                    cv2.imshow('full screen', screen)
                    inv_x_coor = 0
                    
                    for i in range(0, 300, 30):
                        
                        if i+30 <= 300:

                            inv_y_coor = 0
                            for iy in range(0, 120,30):
                                #cv2.imshow('test image {},{}'.format(inv_y_coor,inv_x_coor), np.array(screen[int(iy):int(iy+30), int(i):int(i+30),:]))
                                self.training_data.append([np.array(screen[int(iy):int(iy+30), int(i):int(i+30),:]),inv_labels[inv_y_coor][inv_x_coor]])
                                inv_y_coor +=1
                            inv_x_coor +=1

                    

                    
                    np.save(self.filename,self.training_data)
                            #break
    def __adjusted_capture__(self, screen, base_pixel_x, base_pixel_y, y_size, x_size):
        screen_w_adj = (screen.shape[0]/600)
        screen_h_adj = (screen.shape[1]/800)
        
        aspect_ratio = screen.shape[0]/screen.shape[1]
        aspect_adj = (600/800)/aspect_ratio
        
        screen = np.array(screen[int((base_pixel_y*(1/aspect_adj))*screen_h_adj):int((y_size*(screen.shape[0]/600)+((base_pixel_y*(1/aspect_adj))*screen_h_adj))),
                                int((base_pixel_x*aspect_adj)*screen_w_adj):int((x_size*(screen.shape[1]/800)+(base_pixel_x*aspect_adj)*screen_w_adj)), :])

        screen = cv2.resize(screen,(x_size,y_size))

        return screen
                    
    def monitor_status(self):
        screens = [0,0]
        win32gui.EnumWindows(callback, screens)
        health_statuses = deque(maxlen=15)
        critical_health_count = 0
        #while True:
        with mss.mss() as sct:
            win32gui.EnumWindows(callback, screens)
            monitor = {"top": screens[0][1], "left":screens[0][0], "width": screens[1][0], "height": screens[1][1]}                
            sct_img = sct.grab(monitor)
            
            sct_img = np.array(sct_img)
           
            screen = cv2.cvtColor(sct_img, cv2.IMREAD_GRAYSCALE)

            self.detect_inv_pot(screen)
        return self.inv_labels

    def _detect_health(self, screen): 
        #adjust for resolution neural net was trained on (800X600)
        #health screenshot is 30X90
        screen = self.__adjusted_capture__(screen, 45, 505, 90, 30)
        screen = np.array(screen).reshape(1,90,30,4)
        
        input_array = self.health_model.predict(screen)
        
        pick = np.argmax(input_array)
        
        return self.health_column_names[np.argmax(input_array)]

    def _detect_mana(self, screen): 
        screen = self.__adjusted_capture__(screen, 730, 505, 90, 30)
        screen = np.array(screen).reshape(1,90,30,4)
        input_array = self.mana_model.predict(screen)
        
        pick = np.argmax(input_array)
        
        return self.mana_column_names[np.argmax(input_array)]

    def detect_inv_pot(self, screen): 
        #adjust for resolution neural net was trained on (800X600)
        #health screenshot is 30X90


        screen = self.__adjusted_capture__(screen, 419,317,113,287)
        screen = cv2.resize(screen,(300,120))
        
        inv_x_coor = 0
        for i in range(0, 300, 30):           
            if i+30 <= 300:
                inv_y_coor = 0
                for iy in range(0, 120,30):
                    inv_box = np.array(screen[int(iy):int(iy+30), int(i):int(i+30),:])
                    input_array = self.inv_model.predict(inv_box.reshape(1,30,30,4))
                    
                    self.inv_labels[inv_y_coor][inv_x_coor] = self.itm_labels[np.argmax(input_array)]
                    inv_y_coor +=1
                inv_x_coor +=1
        
        
        #pick = np.argmax(input_array)
        
        #return self.mana_column_names[np.argmax(input_array)]

