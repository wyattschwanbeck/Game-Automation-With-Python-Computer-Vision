from Gradient import  *
from tkinter import StringVar, OptionMenu
from PerspectiveGrid import *

choices = ["red" ,"orange", "yellow", "green", "unset"]

class DigBox (object):
     # String - red, orange, yellow, green, none

    def __init__(self, master, probability=.5, x=None, y=None):

        self.known_color = "unset"
         
        self.probability = probability

        label = StringVar(master)
        label.trace("w", lambda var, index, mode: self._setColorFromLabel())
        self.tkinterLabel = label

        option = OptionMenu(master, self.tkinterLabel, *choices)
        option.config(width=3)
        if (x != None and y != None):
            option.grid(row=y, column=x)
        
        self.tkinterOption = option


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
        return not (self.known_color == "unset" or self.known_color == "green")

        
    def IsSureThing(self):
        return self.known_color == "green"

    def setColor(self, color):
        self.known_color = color
        self._setButtonColor()

    def _setColorFromLabel(self):
        self.known_color = self.tkinterLabel.get()
        self.tkinterLabel.set("")
        self._setButtonColor()

    def _setButtonColor(self):
        colorHex = self.GetButtonColor()
        self.tkinterOption.config(background=colorHex, activebackground=colorHex)


   