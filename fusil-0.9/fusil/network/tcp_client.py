from fusil.network.client import NetworkClient
from socket import AF_INET, SOCK_STREAM

class TcpClient(NetworkClient):
    def __init__(self, project, host, port, connect_timeout=5.0):
        NetworkClient.__init__(self, project, "network:%s:%s" % (host, port))
        self.host = host
        self.port = port
        self.connect_timeout = connect_timeout

    def on_session_start(self):
        self.connect(
            (self.host, self.port),
            AF_INET, SOCK_STREAM,
            timeout=self.connect_timeout)

