#!/usr/bin/env python
# Nolan Liebert, 2008
# See LICENSE and README for details.
from Tkinter import *
import hashlib

root = Tk()
root.title("PySumpas")
root.resizable(0,0)

sv_pwd=StringVar()

def md5gen():
   data1 = t1.get()
   data2 = t2.get()
   m1 = hashlib.md5(data1).hexdigest()
   m2 = hashlib.md5(data2).hexdigest()
   pwd = hashlib.md5(m1 + m2).hexdigest()
   sv_pwd.set(pwd)

def sum1gen():
   data1 = t1.get()
   data2 = t2.get()
   s1 = hashlib.sha1(data1).hexdigest()
   s2 = hashlib.sha1(data2).hexdigest()
   pwd = hashlib.sha1(s1 + s2).hexdigest()
   sv_pwd.set(pwd)

t1 = Entry(root, relief="sunken", width="16")
t1.grid(row=0)

t2 = Entry(root, relief="sunken", width="16")
t2.grid(row=1)

b1 = Button(root, text="Generate MD5", command=md5gen)
b1.grid(row=2, sticky=W)

b2 = Button(root, text="Generate SHA1", command=sum1gen)
b2.grid(row=2, sticky=E)

p = Label(root, relief="sunken", textvariable=sv_pwd, width="40")
p.grid(row=3)

root.mainloop()
