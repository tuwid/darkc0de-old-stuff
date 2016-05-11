from fusil.network.server import TcpServer
from fusil.network.server_client import ServerClientDisconnect
import re

class HttpRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.0"
        self.host = None
        self.headers = []
        self.parse(data)

    def parse(self, data):
        state = "init"
        for line in data.splitlines():
            if state == "init":
                self.parseRequest(line)
                state = "host"
                continue
            if state == "host":
                match = re.match("host: (.*)$", line, re.IGNORECASE)
                if match:
                    self.host = match.group(1)
                    state = "keys"
                    continue
            if not line:
                continue
            line = line.split(":", 1)
            if len(line) == 1:
                raise SyntaxError("Unable to parse client header: %r" % line[0])
            key, value = line
            self.headers.append( (key, value) )

    def parseRequest(self, line):
        # Extract method
        match = re.match("^(GET|POST) (.*)$", line)
        if not match:
            raise SyntaxError("Unable to parse request method: %r" % line)
        line = match.group(2)
        self.method = match.group(1)

        # Extract HTTP version if present
        match = re.match("^(.*) HTTP/(1.[01])$", line)
        if match:
            line = match.group(1)
            self.http_version = match.group(2)

        # Rest is the URI
        self.uri = line

class HttpServer(TcpServer):
    def __init__(self, *args):
        TcpServer.__init__(self, *args)

    def clientRead(self, client):
        # Read data
        try:
            data = client.recvBytes()
        except ServerClientDisconnect, error:
            self.clientDisconnection(client)
            return
        if not data:
            return

        # Process data
        request = HttpRequest(data)
        self.serveRequest(client, request)

    def serveRequest(self, client, request):
        url = request.uri[1:]
        if not url:
            url = "index.html"
        if url == "index.html":
            self.serveData(client, 200, "OK", "<html><body><p>Hello World!</p></body></html>")
        else:
            self.error404(client, url)

    def error404(self, client, url):
        self.warning("Error 404: %r" % url)
        self.serveData(client, 404, "Not Found")

    def serveData(self, client, code, code_text, data=None, content_type="text/html"):
        if data:
            data_len = len(data)
        else:
            data_len = 0
        headers = [
            ("Server", "Fusil"),
            ("Pragma", "no-cache"),
            ("Content-Type", content_type),
            ("Content-Length", str(data_len)),
        ]
        try:
            client.sendBytes("HTTP/1.x %s %s\r\n" % (code, code_text))
            for key, value in headers:
                line = "%s: %s\r\n" % (key, value)
                client.sendBytes(line)
            if data:
                client.sendBytes("\r\n")
                client.sendBytes(data)
            client.close()
        except ServerClientDisconnect, error:
            self.clientDisconnection(client)

