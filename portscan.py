#A simple port scanner to scan a range of ports on a single host.

#Developers:
# 1.Mark Kels (mark.kels@gmail.com) - The basic port scanner
#Last updated:
# 21.5.2005

#----------Imports----------
from Tkinter import * #Used to make the GUI
import tkMessageBox #Used for error display
import socket #Used for connecting to ports
import threading #Used to make a difrent thread for the scan so it could be stopped

#--- Function to start a scan ---
def go():
    global app
    result.delete(1.0,END)
    app=scan()
    app.start() #start() is definde in threading.Thread
#--- Function to stop a scan ---
def stop():
    app.flag='stop'
#--- Function to clear the input and output ---
def clear():
    host_e.delete(0,END)
    start_port_e.delete(0,END)
    end_port_e.delete(0,END)
    result.delete(1.0,END)
    
#---The scan class which does the port scan itself---
class scan(threading.Thread):
    def _init_(self):
        threading.thread._init_(self)
    def run(self):
        self.host=host_e.get() 
        self.start_port=int(start_port_e.get())
        self.end_port=int(end_port_e.get())
        self.open_counter=0
        self.flag='scan'       
        start.config(text="Stop",command=stop)
        root.update()
        result.insert(END,"Scanning "+str(self.host)+"...\n\n")
        root.update()
        while self.start_port<=self.end_port and self.flag=='scan':
            self.sk=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sk.settimeout(0.01) #closed ports take a long time to connect to, so if there is no connection after 0.01 seconds the port is closed
            try:
                self.sk.connect((self.host,self.start_port))
            except:
                pass #if connection fails (port is closed) pass and try with another port
            else:
                result.insert(END,str(self.start_port)+"\n")
                root.update()
                self.open_counter=self.open_counter+1
                self.sk.close()
            self.start_port=self.start_port+1
        if self.flag=='scan':    
            result.insert(END,"\nDone !!\nFound "+str(self.open_counter)+" opened ports")
            root.update()
            start.config(text="Scan",command=go)
            root.update()
        elif self.flag=='stop':
            result.insert(END,"\n Scan stopped.")
            start.config(text="Scan",command=go)
            root.update()

#---The GUI---        
root=Tk()
Label(root,text="Host: ").grid(row=1,column=1,sticky="w")
host_e=Entry(root)
host_e.grid(row=1,column=2,sticky="WE")
Label(root,text="Start port: ").grid(row=2,column=1,sticky="w")
start_port_e=Entry(root)
start_port_e.grid(row=2,column=2,sticky="WE")
Label(root,text="End port: ").grid(row=3,column=1,sticky="w")
end_port_e=Entry(root)
end_port_e.grid(row=3,column=2,sticky="WE")
start=Button(root,text="Scan",command=go)
start.grid(row=5,columnspan=3,sticky="WE")
clear=Button(root,text="Clear",command=clear)
clear.grid(row=6,columnspan=3,sticky="WE")
result=Text(root,width=20,height=20)
result.grid(row=7,columnspan=3,sticky="WENS")


root.wm_maxsize(width='190',height='370') #Set max size
root.wm_minsize(width='190',height='370') #Sat min size same as max size (so the window is unresizeable)
root.title("PPS 0.1") #Set the title of the window

root.mainloop()