from fusil.project_agent import ProjectAgent
from socket import socket, error as socket_error
from fusil.error import formatError, writeError
from fusil.network.tools import formatAddress
from time import time

class NetworkClient(ProjectAgent):
    def __init__(self, project, name):
        ProjectAgent.__init__(self, project, name)
        self.log_data_exchange = True

    def init(self):
        self.socket = None
        self.tx_bytes = 0
        self.rx_bytes = 0

    def connect(self, address, family, type, timeout=5.0):
        try:
            self.info("Create socket (family %s, type %s)" % (
                family, type))
            self.socket = socket(family, type)
            self.socket.settimeout(timeout)
            self.info("Connect to %s" % formatAddress(family, address))
            self.socket.connect(address)
        except socket_error, err:
            writeError(self, err, "Unable to connect to %s" %
                formatAddress(family, address))
            self.socket = None
            self.send('application_error', 'Network connection failure')

    def deinit(self):
        if self.socket:
            self.socket.close()
        info = []
        if self.tx_bytes:
            info.append("TX bytes:%s" % self.tx_bytes)
        if self.rx_bytes:
            info.append("RX bytes:%s" % self.rx_bytes)
        if info:
            self.warning(", ".join(info))

    def sendBytes(self, data, timeout=0):
        if self.socket is None:
            self.error("Error: socket is not initialized!")
            return False
        self.tx_bytes += len(data)
        if self.log_data_exchange:
            self.info("Send bytes: (%s) %r (timeout=%s)" % (
                len(data), data, timeout))
        try:
            self.socket.settimeout(timeout)
            self.socket.send(data)
            return True
        except socket_error, err:
            self.warning("Send error: %s" % formatError(err))
            self.socket = None
            self.send('session_stop')
        return False

    def recvBytes(self, max_size=None, timeout=0.250, buffer_size=1024):
        if self.socket is None:
            self.error("Error: socket is not initialized!")
            return None

        datas = []
        data_len = 0
        time_end = time() + timeout
        while True:
            time_diff = time_end - time()
            if time_diff < 0:
                break
            if max_size is not None and max_size <= data_len:
                break
            try:
                self.socket.settimeout(time_diff)
                data = self.socket.recv(buffer_size)
            except socket_error, err:
                self.warning("Receive error: %s" % formatError(err))
                self.socket = None
                self.send('session_stop')
                break
            if not data:
                break
            self.info("Receive bytes: (%s) %r" % (len(data), data))
            datas.append(data)
            data_len += len(data)
            self.rx_bytes += data_len

        if datas:
            data = ''.join(datas)
            return data
        else:
            return None

