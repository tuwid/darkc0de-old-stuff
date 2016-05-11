from Tkinter import *
import webbrowser
import mytkSimpleDialog

class SupportScreen(mytkSimpleDialog.Dialog):
    def __init__(self, parent, title = None, rootx_offset=50, rooty_offset=50):
        mytkSimpleDialog.Dialog.__init__(self, parent, title, rootx_offset, rooty_offset)

    def body(self, master):
        self.t = Text(master)
        self.t.pack()
        self.t.tag_configure("href", foreground='blue', underline=1)
        self.t.tag_bind("href", "<Button-1>", self.openHREF)
        self.t.tag_bind("href", "<Enter>", self.show_hand_cursor)
        self.t.tag_bind("href", "<Leave>", self.show_arrow_cursor)
        self.t.config(cursor="arrow", bg="SystemButtonFace", wrap=WORD)
        self.t.insert(END, "Welcome to PyKeylogger, a versatile backup and system monitoring solution. \n\n\
PyKeylogger is Free Open Source Software, licensed under the Gnu General Public License. \
You can download the source code from ")
        self.t.insert(END, "http://sourceforge.net/projects/pykeylogger", "href")
        self.t.insert(END, "\n\nHit 'Lcontrol-Rcontrol-F12' to bring up the Control Panel (default password is blank). More help is in the Help menu.\n\n\
Since I am but a poor grad student, \
you are strongly encouraged to donate to this open source project. \
So strongly, in fact, that this program is limited to 4 days of use, and presents you with this nag \
screen every time you start it. \
There is good logic behind why this is being done. If you are curious, you will find the following \
link very informative: ")
        self.t.insert(END, "http://hackvan.com/pub/stig/articles/why-do-people-register-shareware.html", "href")
        self.t.insert(END, "\n\nThere are two ways to get rid of the nag and expiration: \n \
1. Donate to PyKeylogger by following the simple instructions at ")
        self.t.insert(END, "http://pykeylogger.sourceforge.net/wiki/index.php/PyKeylogger:Download_Instructions", "href")
        self.t.insert(END, " and you will get a binary build of PyKeylogger without any nagging, \
by E-mail, HTTP, or FTP.")
        self.t.insert(END, "\n\n 2. Get the source code, then find and toggle the nag control. You can then run \
PyKeylogger from source, or even build your own executable, by following the instructions at ")
        self.t.insert(END, "http://pykeylogger.sourceforge.net/wiki/index.php/PyKeylogger:Installation_Instructions", "href")
        self.t.insert(END, "\n\nFinally, I encourage you to use this software responsibly, keeping to the law and your own moral code.")
        self.t.config(state=DISABLED)

    def show_hand_cursor(self, event):
        self.t.config(cursor="hand2")
    
    def show_arrow_cursor(self, event):
        self.t.config(cursor="arrow")

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        
        box = Frame(self)

        #w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        #w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Continue", width=10, command=self.cancel, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def openHREF(self, event):
        start, end = self.t.tag_prevrange("href", self.t.index("@%s,%s" % (event.x, event.y)))
        #print "Going to %s..." % t.get(start, end)
        webbrowser.open(self.t.get(start, end))


class ExpirationScreen(mytkSimpleDialog.Dialog):
    def __init__(self, parent, title = None, rootx_offset=50, rooty_offset=50):
        mytkSimpleDialog.Dialog.__init__(self, parent, title, rootx_offset, rooty_offset)

    def body(self, master):
        self.t = Text(master)
        self.t.pack()
        self.t.tag_configure("href", foreground='blue', underline=1)
        self.t.tag_bind("href", "<Button-1>", self.openHREF)
        self.t.tag_bind("href", "<Enter>", self.show_hand_cursor)
        self.t.tag_bind("href", "<Leave>", self.show_arrow_cursor)
        self.t.config(cursor="arrow", bg="SystemButtonFace", wrap=WORD)
        self.t.insert(END, "Thank you for using PyKeylogger, a versatile backup and system monitoring solution.")
        self.t.insert(END, "\n\nAs you may remember from reading the \"welcome screen\", this binary expires \
after 4 days of use, as a method of encouraging donations to this open source software project. This installation of \
PyKeylogger has now *EXPIRED*. There are two ways \
to restore PyKeylogger's functionality: \n\n 1. Donate to PyKeylogger by following the simple instructions at ")
        self.t.insert(END, "http://pykeylogger.sourceforge.net/wiki/index.php/PyKeylogger:Download_Instructions", "href")
        self.t.insert(END, " and you will get a binary build of PyKeylogger without any nagscreens or expiration, \
by E-mail, HTTP, or FTP.")
        self.t.insert(END, "\n\n 2. Get the source code, then find and toggle the nag control. You can then run \
PyKeylogger from source, or even build your own executable, by following the instructions at ")
        self.t.insert(END, "http://pykeylogger.sourceforge.net/wiki/index.php/PyKeylogger:Installation_Instructions", "href")
        self.t.insert(END, "\n\nIf you run into any trouble, feel free to ask for help on the PyKeylogger forums: ")
        self.t.insert(END, "http://sourceforge.net/forum/?group_id=147501", "href")
        self.t.config(state=DISABLED)

    def show_hand_cursor(self, event):
        self.t.config(cursor="hand2")
    
    def show_arrow_cursor(self, event):
        self.t.config(cursor="arrow")

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        
        box = Frame(self)

        #w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        #w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Continue", width=10, command=self.cancel, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def openHREF(self, event):
        start, end = self.t.tag_prevrange("href", self.t.index("@%s,%s" % (event.x, event.y)))
        #print "Going to %s..." % t.get(start, end)
        webbrowser.open(self.t.get(start, end))

if __name__ == '__main__':
    # test code
    root=Tk()
    root.geometry("100x100+200+200")
    warn=SupportScreen(root, title="Please Support PyKeylogger", rootx_offset=-20, rooty_offset=-35)
    root.quit()
    
    root=Tk()
    root.geometry("100x100+200+200")
    warn=ExpirationScreen(root, title="PyKeylogger Has Expired", rootx_offset=-20, rooty_offset=-35)
    root.quit()