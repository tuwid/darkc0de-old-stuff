from Tkinter import *
import os
import sys
import time
import win32file
import win32event
import win32con
from threading import *
import tkFileDialog
import Image
import ImageTk
import JpegImagePlugin
import GifImagePlugin
Image.initialized = 1
def realtime_reg():
    #open regmon from with in the app
    p = os.popen("regmon.exe")

def run3():
    #start a thread
    mythread3.start()

def compute():
    #open and read files compare using Lib Diff output to Tk
    textbox.insert(END, "reading files please be patient... This may take a moment\n\n")
    from difflib import Differ
    filename1it = fil1.get()
    filename1it2 = fil2.get()
    filer = open(filename1it, 'rb')
    filer2 = open(filename1it2, 'rb')
    
    data1 = filer.read()
    data2 = filer2.read()
    d = Differ()
    result = list(d.compare(data1, data2))
    textbox.insert(END, "The two files compared with Difflib are " + filename1it + " and " + filename1it2 + "\n\n")
    textbox.insert(END, result)

def run2():
    # start a thread
    mythread2.start() 

###### Begin Code Borrrowed and Modified Info ####################
###### Code borrowed from Tim Golden Python Cookbook 2002/10/11 ######
    

def watchos():
    #get path or maintain current path of app
    FILE_LIST_DIRECTORY = 0x0001
    try: path_to_watch = myos.get() or "."
    except: path_to_watch = "."
    path_to_watch = os.path.abspath(path_to_watch)

    textbox.insert(END, "Watching %s at %s" % (path_to_watch, time.asctime()) + "\n\n")
    # FindFirstChangeNotification sets up a handle for watching
    #  file changes.
    while 1:

        hDir = win32file.CreateFile (
            path_to_watch,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
            )

        change_handle = win32file.ReadDirectoryChangesW (
            hDir,
            1024,
            True,#Heap Size include_subdirectories,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
            )

        # Loop forever, listing any file changes. The WaitFor... will
        #  time out every half a second allowing for keyboard interrupts
        #  to terminate the loop.
        ACTIONS = {
            1 : "Created",
            2 : "Deleted",
            3 : "Updated",
            4 : "Renamed from something",
            5 : "Renamed to something"
            }
        results = change_handle
        for action, files in results:
            full_filename = os.path.join(path_to_watch, files)
            theact = ACTIONS.get(action, "Unknown")
            textbox.insert(END, str(full_filename) + "\t" + str(theact) +"\n")
           
def run():
    # start a thread
    mythread.start()

def save():
    output1 = textbox.get(1.0, END)
    str(output1)
    filename = tkFileDialog.asksaveasfilename()
    fileit = open(filename, "w")
    fileit.write(output1)

def display_help():
    import webbrowser
    webbrowser.open_new("http://www.flyninja.net/book/?p=30")

def display_about():
    top2 = Toplevel(root)
    top2.title("About")
    top2.wm_resizable(0, 0)
    top2.wm_iconbitmap("shinobi.ico")
    top2.minsize(450, 200)
    top2.option_readfile("optionDB")
    frame = Frame(top2)
    label = Label(frame, text="""This Code Copyright Tech Shinobi Productions 2007 - 2008\n
email: admin@techshinobi.com\t web site: www.techshinobi.com""")
    label.pack(side=LEFT)
    frame.pack(fill=BOTH, expand=True)


    

root = Tk()
root.wm_resizable(0, 0)
root.wm_iconbitmap("shinobi.ico")
root.title("Fuct up File Prog")
root.option_readfile("optionDB")
mythread = Thread(target=watchos)
mythread2 = Thread(target=compute)
mythread3 = Thread(target=realtime_reg)
menubar = Menu(root)
# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="How to Use", command=display_help)
helpmenu.add_command(label="About", command=display_about)
menubar.add_cascade(label="Help", menu=helpmenu)


root.config(menu=menubar)
frameverify = Frame(root)
myos = Entry(frameverify)
myos.pack(side=LEFT, fill=BOTH, expand=True)

openit = Label(frameverify, text="Path To Application Install Folder")
openit.pack(side=LEFT)

button = Button(frameverify, text="Watch", command=run)
button.pack(side=LEFT)


openit = Label(frameverify, text="Registry Watching using Regmon.exe")
openit.pack(side=LEFT)



button = Button(frameverify, text="Registry Watch", command=run3)
button.pack(side=LEFT)


frameverify.pack(fill=BOTH, expand=True)


frameverify = Frame(root)
fil1 = Entry(frameverify)
fil1.pack(side=LEFT, fill=BOTH, expand=True)

openit = Label(frameverify, text="Path to original saved Registry file")
openit.pack(side=LEFT)

fil2 = Entry(frameverify)
fil2.pack(side=LEFT, fill=BOTH, expand=True)

openit = Label(frameverify, text="Path to new Registry file")
openit.pack(side=LEFT)

verifyfiles = Button(frameverify, text="Verify/Compare", command=run2)
verifyfiles.pack(side=LEFT)
frameverify.pack(fill=BOTH, expand=True)

frame2 = Frame(root)
scrollbar = Scrollbar(frame2)
scrollbar.pack(side=RIGHT, fill=Y)

textbox = Text(frame2)
textbox.pack(side=LEFT, fill=BOTH, expand=True)
textbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textbox.yview)
frame2.pack(fill=BOTH, expand=True)

root.mainloop()
