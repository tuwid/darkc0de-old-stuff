from Tkinter import *
import random

def randomString():
    mystring = ("A","B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
               "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", \
               "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", \
               "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", \
               "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    try:
        num = int(entry.get())
    except:
        textbox.insert(END, "Failed recieving Length Value\n\n")
    
    r = ''.join(random.sample(mystring, num))
    textbox.insert(END, r + "\n\n")

def clearit():
    try:
        textbox.delete(0.0, END)
    except:
        textbox.insert(END, "Unable to Clear Data\n\n")



root = Tk()
root.title("Password Generator")

frame = Frame(root)
entry = Entry(frame)
entry.pack(side=LEFT)
label = Label(frame, text="Password Length")
label.pack(side=LEFT)
button = Button(frame, text="Generate", command=randomString)
button.pack(side=LEFT)

button2 = Button(frame, text="Clear", command=clearit)
button2.pack(side=LEFT)

frame.pack()
frame2 = Frame(root)
textbox = Text(frame2)
textbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
frame2.pack(expand=TRUE, fill=BOTH)
root.mainloop()
