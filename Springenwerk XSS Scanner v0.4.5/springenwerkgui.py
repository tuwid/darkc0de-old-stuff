"""
Springenwerk Security Scanner GUI

(c)2006 by Johannes Fahrenkrug (jfahrenkrug@gmail.com)
http://springenwerk.org

A GUI for Springenwerk, a Python XSS Scanner.
"""

#Copyright (c) 2006, Johannes Fahrenkrug
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, 
#are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, 
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, 
#      this list of conditions and the following disclaimer in the documentation and/or 
#      other materials provided with the distribution.
#    * Neither the name of Johannes Fahrenkrug and the Springenwerk development team
#      nor the names of its contributors may be used to endorse or promote products 
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
#EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
#OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
#SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
#TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
#BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
#ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
#DAMAGE.

from Tkinter import *
import springenwerk
import tkFileDialog

class SpringenwerkGUI:

    def __init__(self, master):
        
        frame = Frame(master, name="frame")
        frame.pack()
        
        ########## row ##########
        rowIndex = 0
        Label(frame, text="Springenwerk Security Scanner", font=("Helvetica", 16), borderwidth=4, relief=GROOVE).grid(row=rowIndex, column=0, columnspan=5, sticky=E+W)
        
        ########## row ##########
        rowIndex += 1
        Label(frame, text="URL(s), comma seperated:  ").grid(row=rowIndex, column=0, columnspan=1, sticky=W)
        
        self.urlentry = Entry(frame)
        self.urlentry.grid(row=rowIndex, column=1, columnspan=4, sticky=W+E)
        
        ########## row ##########
        rowIndex += 1
        Label(frame, text="User Agent:").grid(row=rowIndex, column=0, columnspan=1, sticky=W)
        
        self.useragent = StringVar(frame)
        self.useragent.set(springenwerk.USERAGENT_SW)

        self.useragentMenu = OptionMenu(frame, self.useragent, springenwerk.USERAGENT_SW, springenwerk.USERAGENT_FF, springenwerk.USERAGENT_IE)
        self.useragentMenu.grid(row=rowIndex, column=1, columnspan=4, sticky=W+E)
        
        ########## row ##########
        rowIndex += 1
        self.browseButtonText = StringVar(frame)
        self.browseButtonText.set("Browse...")
        Label(frame, text="HTML output file:").grid(row=rowIndex, column=0, columnspan=2, sticky=W)
        self.browse = Button(frame, textvariable=self.browseButtonText, command=self.setOutputFile)
        self.browse.grid(row=rowIndex, column=1, columnspan=4, sticky=E+W)
        
        ########## row ##########
        rowIndex += 1
        self.verbose = BooleanVar()
        self.verbose.set(False)
        Checkbutton(frame, text="Verbose", variable=self.verbose, onvalue=True, offvalue=False).grid(row=rowIndex, column=0, sticky=W)
        self.checkargs = BooleanVar()
        self.checkargs.set(False)
        Checkbutton(frame, text="Check Args", variable=self.checkargs).grid(row=rowIndex, column=1, sticky=W)
        self.checkactions = BooleanVar()
        self.checkactions.set(True)
        Checkbutton(frame, text="Check Form Actions", variable=self.checkactions).grid(row=rowIndex, column=2, sticky=W)
        self.withpost = BooleanVar()
        self.withpost.set(False)
        Checkbutton(frame, text="Check POST", variable=self.withpost).grid(row=rowIndex, column=3, sticky=W)
        
        ########## row ##########
        rowIndex += 1
        self.textbox = Text(frame, wrap=NONE)
        self.textbox.grid(row=rowIndex, columnspan=4)
        
        self.scrollVert = Scrollbar(frame, command=self.textbox.yview)
        self.scrollHorz = Scrollbar(frame, command=self.textbox.xview, orient=HORIZONTAL)
        self.scrollVert.grid(row=rowIndex, column=4, sticky=N+S)
        
        ########## row ##########
        rowIndex += 1
        self.scrollHorz.grid(row=rowIndex, column=0, columnspan=4, sticky=W+E)
        
        self.textbox.config(xscrollcommand=self.scrollHorz.set, yscrollcommand=self.scrollVert.set)

        ########## row ##########
        rowIndex += 1
        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.grid(row=rowIndex, column=0, columnspan=2)

        self.start = Button(frame, text="Start", command=self.start)
        self.start.grid(row=rowIndex, column=2, columnspan=2)
        
        self.outputfile = ''
        
        self.write(__doc__)
        self.write("\nFor help, please run the springenwerk.py commandline tool without any arguments\n\n")
        self.write("Springenwerk v" + springenwerk.__version__ + " ready.")
        
    def write(self, txt):        
        self.textbox.insert(END, txt)
        self.textbox.see(END)
        
    def setOutputFile(self):
        self.outputfile = tkFileDialog.asksaveasfilename()
        self.browseButtonText.set(self.outputfile) 

    def start(self):     
        springenwerk.startScan(self.urlentry.get().split(','), 
                               self.outputfile, 
                               self.useragent.get(), 
                               self.verbose.get(), 
                               self.checkargs.get(), 
                               self.withpost.get(),
                               self.checkactions.get())
        print
        print "========================================================="
        print
            

root = Tk()
root.title("Springenwerk v" + springenwerk.__version__)

app = SpringenwerkGUI(root)

sys.stdout = app

root.mainloop()

