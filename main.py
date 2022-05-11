from tkinter import *
#from Collect_Health_Data import *

#listener = Custom_Listener()

master = Tk()
mainframe = Frame(master)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 4)
mainframe.rowconfigure(0, weight = 4)
#mainframe.pack(pady = 100, padx = 100)

master.title("mAEGdIG")

choices = ["red" ,"organge", "yellow", "green", "unset"]


# TODO convert to 10x10 of DigBox object
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


class DigBox (object):
    known_color = "none" # String - red, orange, yellow, green, none
    # etc




def update_colors():
    #TODO iterate through all 100 cells and update probabilities based on known values
    # for each row of menus
    #   for each item of row
    #     calculate and update color of menu
    x = 0


option_menus = []
for y in range(0,10):
    new_row = []
    for x in range(0, 10):
        # TODO access the right DigBox property instead of assigning the whole item e.g. dig_site[y][x].stringVar = StringVar(master)
        dig_labels[y][x] = StringVar(master)
        dig_labels[y][x].trace("w", update_colors())
        option = OptionMenu(master, dig_labels[y][x], *choices)
        option.config(width=6)
        option.grid(row=y, column=x)
        new_row.append(option)
    option_menus.append(new_row)


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


mainloop()

