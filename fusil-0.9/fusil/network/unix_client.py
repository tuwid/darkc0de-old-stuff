from fusil.network.client import NetworkClient
from socket import AF_UNIX, SOCK_STREAM

class UnixSocketClient(NetworkClient):
    def __init__(self, project, socket_filename, connect_timeout=5.0):
        NetworkClient.__init__(self, project, "unix_socket:%s" % socket_filename)
        self.socket_filename = socket_filename
        self.connect_timeout = connect_timeout

    def on_session_start(self):
        self.connect(
            self.socket_filename,
            AF_UNIX, SOCK_STREAM,
            timeout=self.connect_timeout)


