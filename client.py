import xmlrpclib, code
import linecache
# Specify IP of Server here defualt port is 9000
url = "http://localhost:8888"
sock = xmlrpclib.ServerProxy(url)
# use the interactive console to interact example "key.keyit()" will start the logger
interp = code.InteractiveConsole({'key': sock})
interp.interact("Use the keywork, \"key\" to interact with the server")
