from tkinter import *
#from Collect_Health_Data import *
dig_dropdowns = [["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""]]

#listener = Custom_Listener()

master = Tk()
mainframe = Frame(master)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 10)
mainframe.rowconfigure(0, weight = 4)
#mainframe.pack(pady = 100, padx = 100)

master.title("mAEGdIG")

choices = ["red" ,"organge", "yellow", "green", ""]

dig_labels = [["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""]]
def pass_labels():
    labels = []
    for r,row in enumerate(inv_labels,0):
        labels.append([])
        for option in row:
            labels[r].append(str(option.get()))

    listener.collect_ss(labels)

def reset_labels():
    for row in inv_labels:
        for option in row:
            option.set("")

def set_detected_inv():
    detected_labels = listener.monitor_status()

    for r,row in enumerate(detected_labels,0):
        for c,col in enumerate(row,0):
            inv_labels[r][c].set(col)
    
#variable = StringVar(master)
#variable.set("one") # default value

for y in range(0,10):
    for x in range(0, 10):
        dig_labels[y][x] = StringVar(master)
        dig_dropdowns[y][x] = OptionMenu(master, dig_labels[y][x], *choices)
        dig_dropdowns[y][x].config(width=6)
        dig_dropdowns[y][x].grid(row=y, column=x)


class Gradient(object):
    
    Red = 0
    Green = 0
    Blue = 0

    def __init__(self, percentSure):
        red_min = 0.0 
        orange_min = .33
        yellow_min = .66
        green_min = 1
        red = [255,0,0]
        orange = [255, 127, 0]
        yellow = [255,255,0]
        green = [0,255,0]
        if(percentSure<=orange_min):
            Red = 255
            Green= _CalculateRGB((orange_min-percentSure)/(orange_min-red_min), red, orange, red_min, orange_min)
            Blue = 0
            
        elif(percentSure<yellow_min):
            Red=255
            Green = 255
            Blue = _CalculateColor((yellow_min-percentSure)/(yellow_min-orange_min),orange, yellow, orange_min, yellow_min)
        elif(percentSure<green_min):
            Red = _CalculateColor((green_min-percentSure)/(green_min-orange_min),yellow,green,yellow_min, green_min)
            Green= 255
            Blue = 0

    def _CalculateColor(self,percentChange, colorFrom, colorTo, colorFrom_Min, colorTo_Min):
            

                


#capture_button = Button(master, text = "capture inventory", command=pass_labels)
#capture_button.grid(row=5, column=1)

#detect_inv = Button(master, text = "detect inventory", command=set_detected_inv)
#detect_inv.grid(row=5, column=4)

#reset_button = Button(master, text = "reset inventory", command=reset_labels)
#reset_button.grid(row=5, column=8)


#
#w = OptionMenu(master, variable, "one", "two", "three")
#w.pack()

mainloop()

