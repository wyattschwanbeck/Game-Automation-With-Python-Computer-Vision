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
        
        self.health_model = keras.models.load_model('detect_health.h5')
        self.mana_model = keras.models.load_model('detect_mana.h5')
        self.inv_model = keras.models.load_model('Pot_Detection.h5')
        #model.summary()
        self.mouse = Controller()
        self.control = pynput.keyboard.Controller()
        self.health_column_names = ["full health", "slightly hurt", "hurt", "critically hurt"]
        self.mana_column_names = ["full mana", "good mana", "low mana", "no mana"]
        #super(Custom_Listener, self).__init__(self.on_click, self.on_move, self.on_scroll)
        
        self.filename = "training_data/training_environment.npy"
        
        
        if os.path.isfile(self.filename):
            print('File exists, loading previous data!')
            self.training_data = list(np.load(self.filename, allow_pickle=True))
        else:
            print('File does not exist, starting fresh!')
            self.training_data = []
        
        

    def collect_ss(self):
            #while True:
            screens = [0,0]
            win32gui.EnumWindows(callback, screens)
            
            with mss.mss() as sct:
                    inv_labels = [["minor health", "minor health", "minor mana", "minor mana", "super mana", "misc", "misc", "misc", "misc", "misc"],
                                  ["light health", "light health", "light mana", "light mana",  "super mana", "misc", "misc", "misc", "misc", "misc"],
                                  ["health", "health", "mana", "mana", "super health", "misc", "misc", "misc", "misc", "misc"],
                                  ["greater health", "greater health", "greater mana", "greater mana", "super health", "misc", "misc", "misc", "misc", "misc"]]

                                

                    monitor = {"top": screens[0][1], "left":screens[0][0], "width": screens[1][0], "height": screens[1][1]}                
                    sct_img = sct.grab(monitor)
                    
                    sct_img = np.array(sct_img)
                   
                    screen = cv2.cvtColor(sct_img, cv2.IMREAD_GRAYSCALE)
                    #screen = cv2.resize(sct_img, (50,40))
                    if len(self.training_data)%100==0:
                        print(len(self.training_data))
                    screen = screen[315:435, 422:712, :]
                    #self.training_data.append([np.array(screen),"no mana"])
                    inv_x_coor = 0
                    
                    for i in range(0, 290, 29):
                        if i+29 <= 290:

                            inv_y_coor = 0
                            for iy in range(0, 120,30):
                                #cv2.imshow('test image {}'.format(inv_labels[inv_y_coor][inv_x_coor]), np.array(screen[int(iy):int(iy+30), int(i):int(i+29),:]))
                                #self.training_data.append([np.array(screen[int(iy):int(iy+30), int(i):int(i+29),:]),inv_labels[inv_y_coor][inv_x_coor]])
                                inv_y_coor +=1
                            inv_x_coor +=1

                    

                    if len(self.training_data)%20000 == 0:
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
        #cv2.imshow("test window", np.array(screen))
        screen = np.array(screen).reshape(1,x_size,y_size,4)

        return screen
                    
    def monitor_status(self):
        screens = [0,0]
        win32gui.EnumWindows(callback, screens)
        health_statuses = deque(maxlen=15)
        critical_health_count = 0
        while True:
            with mss.mss() as sct:
                win32gui.EnumWindows(callback, screens)
                monitor = {"top": screens[0][1], "left":screens[0][0], "width": screens[1][0], "height": screens[1][1]}                
                sct_img = sct.grab(monitor)
                
                sct_img = np.array(sct_img)
               
                screen = cv2.cvtColor(sct_img, cv2.IMREAD_GRAYSCALE)

                #print(screens)

                #cv2.imshow('test image', screen)
                #break

                #health_statuses.append(self.detect_health(screen))
                #break
                print(self.detect_mana(screen))
                
                health_status = self.detect_health(screen)
                mana_status = self.detect_mana(screen)

                print("health: {} | mana: {}".format(health_status, mana_status))
                
                #if (health_status !="critically hurt"):
                #    critical_health_count = 0
                #else:
                #    critical_health_count += 1
                    
                #if (5 < critical_health_count):
                    #self.chicken(screens)
                    #break

    def detect_health(self, screen): 
        #adjust for resolution neural net was trained on (800X600)
        #health screenshot is 30X90
        screen = self.__adjusted_capture__(screen, 45, 505, 90, 30)
        
        input_array = self.health_model.predict(screen)
        
        pick = np.argmax(input_array)
        
        return self.health_column_names[np.argmax(input_array)]

    def detect_mana(self, screen): 
        screen = self.__adjusted_capture__(screen, 730, 505, 90, 30)

        input_array = self.mana_model.predict(screen)
        
        pick = np.argmax(input_array)
        
        
        return self.mana_column_names[np.argmax(input_array)]

    def detect_inv_pot(self, screen): 
        #adjust for resolution neural net was trained on (800X600)
        #health screenshot is 30X90
        inv_labels = [
                    ["", "", "", "","","","","","",""],
                    ["", "", "", "","","","","","",""],
                    ["", "", "", "","","","","","",""],
                    ["", "", "", "","","","","","",""]
                    ]

        screen = self.__adjusted_capture__(screen, 422, 315, 120, 290)

        inv_x_coor = 0
        for i in range(0, 290, 29):
            if i+29 <= 290:

                inv_y_coor = 0
                for iy in range(0, 120,30):
                    #cv2.imshow('test image {}'.format(inv_labels[inv_y_coor][inv_x_coor]), np.array(screen[int(iy):int(iy+30), int(i):int(i+29),:]))
                    #self.training_data.append([np.array(screen[int(iy):int(iy+30), int(i):int(i+29),:]),inv_labels[inv_y_coor][inv_x_coor]])
                    
                    inv_y_coor +=1
                inv_x_coor +=1
        
        
        #pick = np.argmax(input_array)
        
        #return self.mana_column_names[np.argmax(input_array)]

        


listener = Custom_Listener()
#listener.collect_ss()
listener.monitor_status()
