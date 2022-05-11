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
    def __init__(self, percentSure):
        #Provides gradient of color based on interative color scales 1-100%
        # red, orange, yellow, and green
        self.red = 0
        self.green = 0
        self.blue = 0
        red_min = 0.0 
        orange_min = .33
        yellow_min = .66
        green_min = 1
        red_list = [255,0,0]
        orange_list = [255, 127, 0]
        yellow_list = [255,255,0]
        green_list = [0,255,0]

        if(percentSure<=orange_min):
            self.red = 255
            self.green= ((orange_min-percentSure)/(orange_min-red_min) * (orange_list[1]-red_list[1]))+red_list[1]
            self.blue = 0
            
        elif(percentSure<yellow_min):
            self.red=255
            self.green = 255
            self.blue = ((yellow_min-percentSure)/(yellow_min-orange_min) * (yellow_list[2]-orange_list[2]))+orange_list[2]

        elif(percentSure<green_min):
            self.red = ((green_min-percentSure)/(green_min-yellow_min) * (green_list[0]-yellow_list[0]))+yellow_list[0]
            self.green= 255
            self.blue = 0

                
def _from_rgb(self):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % (self.red, self.green, self.blue)   

mainloop()

