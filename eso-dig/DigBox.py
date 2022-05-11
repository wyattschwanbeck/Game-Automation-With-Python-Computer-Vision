from Gradient import  *
from tkinter import StringVar

class DigBox (object):
     # String - red, orange, yellow, green, none

    def __init__(self, probability=.5):
        self.known_color = "unset"
         
        self.probability = .5

    def GetFrameColor(self):
        return Gradient(0 if self.RuledOut else 1 if self.SureThing else self.probability)

    def GetButtonColor(self):
        red = (255,0,0)
        orange = (255, 127, 0)
        yellow = (255,255,0)
        green = (0,255,0)
        if(self.known_color == "red"):
            return "#%02x%02x%02x" % red
        elif(self.known_color == "orange"):
            return "#%02x%02x%02x" % orange
        elif(self.known_color == "yellow"):
            return "#%02x%02x%02x" % yellow
        elif(self.known_color == "green"):
            return "#%02x%02x%02x" % green
        else:
            return "#%02x%02x%02x" % (255,255,255)

    def IsRuledOut(self):
        if(self.known_color == "unset" or self.known_color == "green"):
            return False
        else:
            return True

        
    def IsSureThing(self):
        if(self.known_color == "green"):
            return True
        else:
            return False


