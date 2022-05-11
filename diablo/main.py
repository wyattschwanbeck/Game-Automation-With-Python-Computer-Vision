from tkinter import *
from Collect_Health_Data import *
inv_dropdowns = [["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""],
              ["", "", "", "", "", "", "", "", "", ""]]
listener = Custom_Listener()

master = Tk()
mainframe = Frame(master)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 10)
mainframe.rowconfigure(0, weight = 4)
#mainframe.pack(pady = 100, padx = 100)

master.title("D2 Inventory Capture for Neural Network Training")

choices = [ '', 'misc',
            'minor health','minor mana',
            'light health','light mana',
            'mana', 'health',
            'greater health','greater mana',
            'super health','super mana',
            'rejuv', 'full rejuv'
            ]

inv_labels = [["", "", "", "", "", "", "", "", "", ""],
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

for y in range(0,4):
    for x in range(0, 10):
        inv_labels[y][x] = StringVar(master)
        inv_dropdowns[y][x] = OptionMenu(master, inv_labels[y][x], *choices)
        inv_dropdowns[y][x].config(width=6)
        inv_dropdowns[y][x].grid(row=y, column=x)
        
capture_button = Button(master, text = "capture inventory", command=pass_labels)
capture_button.grid(row=5, column=1)

detect_inv = Button(master, text = "detect inventory", command=set_detected_inv)
detect_inv.grid(row=5, column=4)

reset_button = Button(master, text = "reset inventory", command=reset_labels)
reset_button.grid(row=5, column=8)


#
#w = OptionMenu(master, variable, "one", "two", "three")
#w.pack()

mainloop()