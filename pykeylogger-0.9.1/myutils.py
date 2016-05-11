import zlib
import base64
import sys
import imp

def password_obfuscate(password):
    return base64.b64encode(zlib.compress(password))
def password_recover(password):
    return zlib.decompress(base64.b64decode(password))

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") or # old py2exe
            imp.is_frozen("__main__")) # tools/freeze


#~ if __name__ == '__main__':
    #some test code here. 
    #~ def hello(name="bla"):
        #~ print "hello, ", name

    #~ myt = MyTimer(1.0, 5, hello, ["bob"])
    #~ myt.start()
    #~ time.sleep(4)
    #~ myt.cancel()
    #~ print "next timer"
    #~ myt = MyTimer(1.0, 0, hello, ["bob"])
    #~ myt.start()
    #~ time.sleep(6)
    #~ myt.cancel()
