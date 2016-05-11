from fusil.network.tools import formatAddress
from fusil.session_agent import SessionAgent
from socket import error as socket_error, timeout as socket_timeout
from fusil.error import formatError

class ServerClientDisconnect(Exception):
    pass

class ServerClient(SessionAgent):
    def __init__(self, session, socket, address, family):
        self.socket = socket
        self.address = address
        self.family = family
        name = "net_client:" + formatAddress(self.family, self.address, short=True)
        SessionAgent.__init__(self, session, name)
        self.tx_bytes = 0
        self.rx_bytes = 0

    def recvBytes(self, buffer_size=1024):
        datas = []
        while True:
            try:
                self.socket.settimeout(0.010)
                data = self.socket.recv(buffer_size)
            except socket_timeout:
                break
            except socket_error, err:
                errcode = err[0]
                if errcode == 11: # Resource temporarily unavailable
                    break
                else:
                    self.close()
                    return None
            if not data:
                break
            data_len = len(data)
            self.rx_bytes += data_len
            self.debug("Read bytes: (%s) %r" % (data_len, data))
            datas.append(data)

        if not datas:
            self.close()
            return None
        return ''.join(datas)

    def sendBytes(self, data, buffer_size=4096):
        data_queue = data
        while data_queue:
            data = data_queue[:buffer_size]
            self.tx_bytes += len(data)
            self.debug("Send bytes: (%s) %r" % (len(data), data))
            try:
                self.socket.send(data)
            except socket_error, err:
                self.warning("Send error: %s" % formatError(err))
                self.close()
            data_queue = data_queue[buffer_size:]

    def close(self, emit_exception=True):
        self.socket.close()
        self.socket = None
        if emit_exception:
            raise ServerClientDisconnect()

    def destroy(self):
        if self.socket:
            self.close(False)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<%s %s>" % (
            self.__class__.__name__,
            formatAddress(self.family, self.address))

