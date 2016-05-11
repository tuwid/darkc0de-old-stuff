from threading import *
from Tkinter import *
import time
def netstat_func():
    import subprocess
    while 1:
        p = subprocess.Popen(['netstat', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        for entry in out:
            listb.insert(END, "\n".join(entry))
        listb.select_set(0)
        time.sleep(10.0)
        listb.delete(1.0, END)
    




root = Tk()
root.wm_resizable(0, 0)
root.minsize(600, 400)
#root.wm_iconbitmap("shinobi.ico")
root.title("Tech Shinobi Netstat Tool")
#root.option_readfile("optionDB")
mythread = Thread(target=netstat_func)

frame2 = Frame(root, background="#ffffff")
scrollbar2 = Scrollbar(frame2)
scrollbar2.pack(side=LEFT, fill=Y)

listb = Text(frame2)
listb.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar2.config(command=listb.yview)
listb.config(yscrollcommand=scrollbar2.set)
frame2.pack(fill=BOTH, expand=True)
mythread.start()
root.mainloop()
