from fusil.project_agent import ProjectAgent
from fusil.network.server_client import ServerClient
from fusil.network.tools import formatAddress
from socket import (socket, error as socket_error,
    AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR)
from fusil.error import writeError
from select import select

class NetworkServer(ProjectAgent):
    CLIENT_CLASS = ServerClient

    def __init__(self, project, name):
        ProjectAgent.__init__(self, project, name)
        self.log_data_exchange = True
        self.backlog = 1
        self.client_class = self.CLIENT_CLASS
        self.socket = None
        self.family = None
        self.clients = []

    def bind(self, address, family=AF_INET, type=SOCK_STREAM, reuse_address=True):
        try:
            self.socket = socket(family, type)
            if reuse_address:
                self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.family = family
            self.socket.bind(address)
            self.socket.listen(self.backlog)
            self.error("Server waiting on %s" % formatAddress(family, address))
        except socket_error, err:
            writeError(self, err, "Unable to bind on %s" %
                formatAddress(family, address))
            self.socket = None
            self.send('application_error', 'Network server bind error')

    def destroy(self):
        if self.socket:
            self.socket.close()

    def acceptClient(self):
        client_socket, client_address = self.socket.accept()
        client = self.client_class(
            self.project().session,
            client_socket, client_address,
            self.family)
        self.warning("New client: %s" % client)
        self.clients.append(client)

    def clientDisconnection(self, client):
        if client not in self.clients:
            return
        self.info("Client closed: %r" % client)
        self.clients.remove(client)

    def clientRead(self, client):
        data = client.recvBytes()

    def live(self):
        server_fileno = self.socket.fileno()
        read_fds = [server_fileno]
        client_fds = dict( (client.socket.fileno(), client) for client in self.clients )
        read_fds += client_fds.keys()
        read_available = select(read_fds, [], [], 0)[0]
        if read_available is None:
            return
        for fd in read_available:
            if fd in client_fds:
                client = client_fds[fd]
                self.info("Read data from %s" % client)
                self.clientRead(client)
            else:
                self.info("Accept client")
                self.acceptClient()

class TcpServer(NetworkServer):
    def __init__(self, project, port, host=''):
        name = "tcp_server:" + formatAddress(AF_INET, (host, port), short=True)
        NetworkServer.__init__(self, project, name)
        self.host = host
        self.port = port
        self.bind(address=(self.host, self.port))

