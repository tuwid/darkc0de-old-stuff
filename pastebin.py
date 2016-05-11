# Uploads source files to pastebin.com 
# or other subdomain of pastebin. Supports
# several filetypes. Username and subdomain
# constants provided.  In order to use this 
# to its full potential you can make some registry 
# edits to allow a right click 'Upload To Pastebin' 
# option. I will have a script that automates that for you.
# Until then follow this guide 
#     http://www.jfitz.com/tips/rclick_custom.html
#
# This is the value I used in my registry:
# C:\Python26\pythonw.exe  C:\Python26\pastebin.py "%1"
#
# Enjoy, 
# LogicKills


import urllib
import httplib
import sys
import string
import os.path

# Constants
URL = "http://SubDomain.pastebin.com"  
USER = "darkc0de supporter"


# Returns actual source code from file
def readFile():
   fileIn = open(sys.argv[1],"r")
   content = fileIn.read()
   return content

# Returns the file's extension (ex: .cpp)
def getExtension():
   fileName = sys.argv[1]
   extension = os.path.splitext(fileName)[1]
   return extension

# Returns extensions corelated label
def getCodeType(ext):
   codeType = ""
   extensions = [
      ".py","python",
      ".cpp","cpp",
      ".sh","bash",
      ".pl","perl",
      ".php","php",
      ".LUA","lua",
      ".js", "javascript",
      ".java","java",
      ".html","html4strict",
      ".cs","csharp"
      ]
      
   x = 0
   while x < 5:
      if extensions[x] == ext:
         codeType = extensions[x + 1]
         break
      else:
         x += 2
   
   return codeType
      
   
   
   
def postIt(codeType,theCode):
   POST = "/pastebin.php parent_pid=&format=" + codeType + "&code2=" + theCode + "&poster=" + USER + "&paste=Send&expiry=f&email="
   
   urllib.urlopen(URL,POST);
   

def main():
   content = readFile()
   extension = getExtension()
   codeType = getCodeType(extension)
   postIt(codeType,content)
   

   
if __name__ == "__main__":
   main()
