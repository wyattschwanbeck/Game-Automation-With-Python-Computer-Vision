from tkinter import *
from DigBox import *
#from Collect_Health_Data import *

#listener = Custom_Listener()

master = Tk()
mainframe = Frame(master)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 4)
mainframe.rowconfigure(0, weight = 4)
#mainframe.pack(pady = 100, padx = 100)

master.title("mAEGdIG")

choices = ["red" ,"orange", "yellow", "green", "unset"]


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


def update_colors(var, index, mode):
    #TODO iterate through all 100 cells and update probabilities based on known values
    # for each row of menus
    #   for each item of row
    #     calculate and update color of menu
    
    x =0

def update_dig_Box(var, index, mode):
    for y in range(0,10):
        for x in range(0, 10):
            dig_box[y][x].known_color = dig_labels[y][x].get()
            option_menus[y][x].config(background=dig_box[y][x].GetButtonColor())
    


dig_box = []
option_menus = []
for y in range(0,10):
    new_row = []
    new_dig_row = []
    for x in range(0, 10):
        # TODO access the right DigBox property instead of assigning the whole item e.g. dig_site[y][x].stringVar = StringVar(master)
        dig_labels[y][x] = StringVar(master)
        dig_labels[y][x].trace("w", update_colors)
        dig_box.append(new_dig_row)
        option = OptionMenu(master, dig_labels[y][x], *choices)
        option.config(width=6)
        option.grid(row=y, column=x)
        new_row.append(option)
        new_dig_row.append(DigBox())
    option_menus.append(new_row)

for y in range(0,10):
    for x in range(0, 10):
        dig_labels[y][x].trace("w", update_dig_Box)




mainloop()

