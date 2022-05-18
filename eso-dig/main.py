from tkinter import *
from DigBox import *
from PerspectiveGrid import *
#from Collect_Health_Data import *

#listener = Custom_Listener()

master = Tk()
mainframe = Frame(master)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 4)
mainframe.rowconfigure(0, weight = 4)
#mainframe.pack(pady = 100, padx = 100)

master.title("mAEGdIG")


# 10 x 10 array of DigBox
dig_boxes = [[DigBox(master, x=i, y=j) for i in range(10)] for j in range (10)]

def setColorsFromCapture():#var, index, mode):
    capture = PerspectiveGrid()
    for y in range(0,10):
        for x in range(0,10):
            dig_boxes[y][x].setColor("")


    for matchKey in capture.Matches.keys():
        for coord in capture.Matches[matchKey]:
            x = min(int(coord[0]),9)
            y = min(int(coord[1]),9)
            dig_boxes[y][x].setColor(matchKey)

    # print("done")
        

capture_button = Button(master, text = "capture inventory", command=setColorsFromCapture)
capture_button.grid(row=11, column=1)



mainloop()

