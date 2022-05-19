from stringprep import c22_specials
import cv2
import numpy as np
import mss
from matplotlib import pyplot as plt
import math
class PerspectiveGrid(object):
    
    def __init__(self):
        #https://realpython.com/python-opencv-color-spaces/
        self.img = self._captureMainScreen()
        
        self.img_hsv = cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV)
        green_min = (49,110,248)
        green_max = (83,255,255)
        self.Matches = {}
        self.indexedMatches = {}
        self.FindMatchingGrid("green",green_min,green_max, 50)
        red_min = (0,167,122)
        red_max = (6,189,255)
        self.FindMatchingGrid("red",red_min,red_max,5)
        orange_min = (13,127,244)
        orange_max = (20,148,255)
        self.FindMatchingGrid("orange",orange_min,orange_max,8)
        yellow_min = (28,142,187)
        yellow_max = (31,159,248)
        self.FindMatchingGrid("yellow",yellow_min,yellow_max,50)



    def _captureMainScreen(self):
        with mss.mss() as sct:
            # The screen part to capture
            monitor_number = 2
            mon = sct.monitors[monitor_number]

            # The screen part to capture
            monitor = {
                "top": mon["top"],  # 100px from the top
                "left": mon["left"],  # 100px from the left
                "width": 1920,
                "height": 1080,
                "mon": monitor_number,
            }
            
            # Grab the data
            img = np.array(sct.grab(monitor))
            #Transform perspective
            # https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
            rows,cols,ch = img.shape
            pts1 = np.float32([ [1384, 991],[1320, 223], [534, 989], [662, 223]])
            pts2 = np.float32([[0,0],[1390,0],[0,1390],[1380,1265]])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(img,M,(1390,1390))
            #dst = cv2.rotate(cv2.cvtColor(dst,cv2.COLOR_BGR2RGB), cv2.cv2.ROTATE_90_CLOCKWISE)
            dst = cv2.flip(cv2.flip(cv2.cvtColor(dst,cv2.COLOR_BGR2RGB),0),1)
            cv2.imwrite( "C:\\Users\\wyatt\\source\\repos\\Diablo-2-Pots-Monitor-with-TensorFlow\\eso-dig\\Test.png",cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))

            return dst
    
    def FindMatchingGrid(self, color_name, min_hsv, max_hsv, color_threshold):
           grid_mask = cv2.inRange(self.img_hsv, min_hsv, max_hsv)
           result = cv2.bitwise_and(self.img, self.img, mask=grid_mask)
           gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
           self.Matches[color_name] = []
           thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
           
           #https://stackoverflow.com/questions/55169645/square-detection-in-image
           #cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
           #cnts = cnts[0] if len(cnts) == 2 else cnts[1]
           min_area = 150
           max_area = 200
           image_number = 0
           matches = []
           x_width = round(result.shape[0]/10)
           y_width = round(result.shape[1]/10)
           og_thresh = color_threshold
           print(color_name)
           for y_index in range(0,10):
               for x_index in range(0,10):
                #if((x_index==0 and y_index==0) or (y_index==10 and x_index==10)):
                #matched_total = np.count_nonzero(gray[(x_index*(x_width)):(x_index+1)*(x_width),y_index*(y_width):(y_index+1)*(y_width)])
                #matched_top = np.count_nonzero(gray[int((x_index)*(x_width)):int((x_index+1))*(x_width),int((y_index))*(y_width):int((y_index+.5)*(y_width))])
                #matched_right = np.count_nonzero(gray[int((x_index+.5)*(x_width)):(x_index+1)*(x_width),int((y_index)*(y_width)):int((y_index+1)*(y_width))])
                #matched_bottom = np.count_nonzero(gray[int((x_index)*(x_width)):(x_index+1)*(x_width),int(y_index+.5)*(y_width):int((y_index+1)*(y_width))])
                #matched_left = np.count_nonzero(gray[int((x_index)*(x_width)):int((x_index+.5)*(x_width)),int(y_index)*(y_width):int((y_index+1)*(y_width))])
                #else:
                
                matched_total = np.count_nonzero(thresh[(x_index*(x_width)):(x_index+1)*(x_width),y_index*(y_width):(y_index+1)*(y_width)])
                matched_top = np.count_nonzero(thresh[int((x_index+.05)*(x_width)):int((x_index+.95))*(x_width),y_index*(y_width):int((y_index+.5)*(y_width))])
                matched_right = np.count_nonzero(thresh[int((x_index+.5)*(x_width)):(x_index+1)*(x_width),int((y_index+.05)*(y_width)):int((y_index+.95)*(y_width))])
                matched_bottom = np.count_nonzero(thresh[int((x_index+.05)*(x_width)):int((x_index+.95)*(x_width)),int(y_index+.5)*(y_width):int((y_index+1)*(y_width))])
                matched_left = np.count_nonzero(thresh[int((x_index)*(x_width)):int((x_index+.5)*(x_width)),int(y_index+.05)*(y_width):int((y_index+.95)*(y_width))])
                
                #if(x_index==0 or y_index ==0):
                #    if(matched_right>color_threshold and matched_top>color_threshold):
                #        matched = True
                #    elif(matched_right>color_threshold and matched_bottom>color_threshold):
                #        matched = True
                #    elif(matched_top>color_threshold and matched_left>color_threshold):
                #        matched = True
                #    elif(matched_top>color_threshold and matched_bottom>color_threshold):
                #        matched = True
                #    elif(matched_left>color_threshold and matched_right>color_threshold):
                #        matched = True
                    #elif(matched_bottom>color_threshold and matched_right>color_threshold):
                #    else:
                #        matched = True
                #else:
                if(matched_top>color_threshold and matched_left>color_threshold and matched_right>color_threshold and matched_bottom>color_threshold):
                    matched = True
                elif( matched_left>color_threshold and matched_right>color_threshold and matched_bottom>color_threshold):
                    matched = True
                elif(matched_top>color_threshold and matched_right>color_threshold and matched_bottom>color_threshold):
                    matched = True
                elif(matched_top>color_threshold and matched_left>color_threshold and matched_bottom>color_threshold):
                    matched = True
            

            #((matched_left>color_threshold and matched_top>color_threshold and matched_bottom>color_threshold)):
                    matched = True
            #elif(matched_top>color_threshold and matched_bottom>color_threshold) or (matched_left>color_threshold and matched_right>color_threshold):
                    matched = True
                else:
                    matched = False

                if(matched):
                    #cv2.imwrite('C:\\Users\\wyatt\\source\\repos\\Diablo-2-Pots-Monitor-with-TensorFlow\\eso-dig\\ROI_{}_X{}_Y{}.png'.format(color_name, x_index, y_index), gray[x_index*(x_width):(x_index+1)*(x_width),y_index*(y_width):(y_index+1)*(y_width)])
                    #cv2.rectangle(self.img, (x, y), (x + w, y + h), (36,255,12), 2)
                    image_number += 1
                    
                    #x_index = round((y)/y_width)
                    #y_index = round((x)/x_width)
                    #print("{0} - {1} {2}".format(color_name, x_index, y_index))
                    self.Matches[color_name].append((x_index,y_index))
                    indexLookup = "{0} , {1}".format(x_index,y_index)
                    if(indexLookup in self.indexedMatches.keys() ):
                        self.indexedMatches[indexLookup].append(color_name)
                    else:
                        self.indexedMatches[indexLookup] = []
                        self.indexedMatches[indexLookup].append(color_name)
          
#Boxes_Min = (0,135,177)
#Boxes_Max = (179, 255, 255)




#green_mask = cv2.inRange(self.img_hsv, green_min, green_max)
#orange_mask = cv2.inRange(dst_hsv, orange, yellow)
#green_mask = cv2.inRange(dst_hsv, yellow, green)
#from matplotlib import pyplot as plt
#plt.subplot(1, 2, 1)
#result = cv2.bitwise_and(dst, dst, mask=red_mask)

#plt.imshow(red_mask, cmap="gray")
#plt.subplot(1, 2, 2)
#plt.imshow(result)
#plt.show()

#cv2.imwrite( "C:\\Users\\wyatt\\source\\repos\\Diablo-2-Pots-Monitor-with-TensorFlow\\eso-dig\\Test.png",cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
