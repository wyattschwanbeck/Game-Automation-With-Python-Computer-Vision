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
mainframe.columnconfigure(0, weight = 4)
mainframe.rowconfigure(0, weight = 4)
#mainframe.pack(pady = 100, padx = 100)

master.title("mAEGdIG")

choices = ["red" ,"organge", "yellow", "green", "unset"]

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


def update_colors():
    #TODO
    x = 0
    
#variable = StringVar(master)
#variable.set("one") # default value

for y in range(0,10):
    for x in range(0, 10):
        dig_labels[y][x] = StringVar(master)
        dig_labels[y][x].trace("w", update_colors())
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
            Green= ((orange_min-percentSure)/(orange_min-red_min) * (orange[1]-red[1]))+red[1]
            Blue = 0
            
        elif(percentSure<yellow_min):
            Red=255
            Green = 255
            Blue = ((yellow_min-percentSure)/(yellow_min-orange_min) * (yellow[2]-orange[2]))+orange[2]
        elif(percentSure<green_min):
            Red = ((green_min-percentSure)/(green_min-yellow_min) * (green[0]-yellow[0]))+yellow[0]
            Green= 255
            Blue = 0

                


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

