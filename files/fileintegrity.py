from Tkinter import *
import tkFileDialog
import md5, os, time

def opendirectory():
    try:
        entry.delete(0, END)
        fileopen = tkFileDialog.askdirectory()
        entry.insert(END, fileopen)
    except:
        textbox.insert(END, "There was an error opening ")
        textbox.insert(END, fileopen)
        textbox.insert(END, "\n")

def saveit():
    try:
        output1 = textbox.get(1.0, END)
        str(output1)
        filename = tkFileDialog.asksaveasfilename()
        entry2.insert(END, filename)
        fileit = open(filename, "w")
        fileit.write(output1)
    except:
        textbox.insert(END, "Failed Saving Data\n")

def windowit():
    top = Toplevel(root)
    top.title("Save Data")
    top.wm_resizable(0, 0)
    top.wm_iconbitmap("shinobi.ico")
    frame = Frame(top)
    global entry2
    entry2 = Entry(frame)
    entry2.pack(side=LEFT)
    entry2.insert(END, "Path Automatically Inserted")
    savebutton = Button(frame, text="Save Reference", command=saveit)
    savebutton.pack(side=LEFT)
    frame.pack()


def compute():
    from difflib import Differ
    filename1it = fil1.get()
    filename1it2 = fil2.get()
    filer = open(filename1it, 'rb')
    filer2 = open(filename1it2, 'rb')
    data1 = filer.read()
    data1 = data1.rstrip()
    data2 = filer2.read()
    data2 = data2.rstrip()
    d = Differ()
    result = list(d.compare(data1, data2))
    s = "\n".join(result)
    s = s.rstrip()
    textbox.insert(END, "The two files compared with Difflib are " + filename1it + " and " + filename1it2 + "\n\n")
    textbox.insert(END, s)
  


def create():
    for root, dirs, files in os.walk(entry.get()):
        for name in files:
            filepath = os.path.join(root, name)
            global value
            value = md5.new(filepath).hexdigest()
            textbox.insert(END, value +"\n")




root = Tk()
root.wm_resizable(0, 0)
root.wm_iconbitmap("shinobi.ico")
root.title("Tech Shinobi File System Integrity Tools")
root.option_readfile("optionDB")
frame = Frame(root)
entry = Entry(frame)
entry.pack(side=LEFT, fill=X, expand=True)

openit = Button(frame, text="Open Directory", command=opendirectory)
openit.pack(side=LEFT)
createit = Button(frame, text="Create MD5", command=create)
createit.pack(side=LEFT)
save = Button(frame, text="Save", command=windowit)
save.pack(side=LEFT)

frame.pack(fill=X, expand=True)

frameverify = Frame(root)
fil1 = Entry(frameverify)
fil1.pack(side=LEFT, fill=X, expand=True)

openit = Label(frameverify, text="Path to original saved file")
openit.pack(side=LEFT)

fil2 = Entry(frameverify)
fil2.pack(side=LEFT, fill=X, expand=True)

openit = Label(frameverify, text="Path to new saved file")
openit.pack(side=LEFT)

verifyfiles = Button(frameverify, text="Verify/Compare", command=compute)
verifyfiles.pack(side=LEFT)
frameverify.pack(fill=X, expand=True)

frame2 = Frame(root)
scrollbar = Scrollbar(frame2)
scrollbar.pack(side=RIGHT, fill=Y)

textbox = Text(frame2)
textbox.pack(side=LEFT, fill=BOTH, expand=True)
textbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textbox.yview)
frame2.pack(fill=BOTH, expand=True)

root.mainloop()
