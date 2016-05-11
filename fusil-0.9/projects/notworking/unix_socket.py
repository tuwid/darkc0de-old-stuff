"""
Pure random UNIX socket fuzzer
"""

def setupProject(project):
#    filename, process_name = "", ""
#    filename, process_name = "/tmp/.X11-unix/X0", "X"
    filename, process_name = "/var/run/acpid.socket", "[kacpid]"
#    filename, process_name = "/var/run/mysqld/mysqld.sock", "mysqld"
#    filename, process_name = "/var/run/sdp", "hcid"
#    filename, process_name = "/var/run/xdmctl/dmctl-:0/socket", "kdm"

    AcpidSocket(project, filename)
    process = AttachProcess(project, process_name)
    process.max_memory = 500*1024*1024

    Syslog(project)

from fusil.network.unix_client import UnixSocketClient
from fusil.bytes_generator import BytesGenerator
from fusil.process.attach import AttachProcess
from fusil.linux.syslog import Syslog
from random import randint

class AcpidSocket(UnixSocketClient):
    def __init__(self, project, *args):
        UnixSocketClient.__init__(self, project, *args)
        max_size = 100
        self.data_gen = BytesGenerator(1, max_size)
        self.max_tx_bytes = max_size * 20
        self.max_rx_bytes = max_size * 20

    def live(self):
        if (self.max_tx_bytes < self.tx_bytes) \
        or (self.max_rx_bytes < self.rx_bytes):
            self.error("MAX! (RX=%s TX=%s)" % (
                self.rx_bytes, self.tx_bytes))
            self.send('session_stop')
            self.socket = None
            return
        if not self.socket:
            return
        action = randint(0, 2)
        if action == 0:
            self.actionSend()
        elif action == 1:
            self.actionReceive()
        else:
            self.actionSend()
            if not self.socket:
                return
            self.actionReceive()

    def actionSend(self):
        data = self.data_gen.createValue()
        self.warning("Send %s bytes: %r" % (len(data), data))
        self.sendBytes(data)

    def actionReceive(self):
        data = self.recvBytes(timeout=0)
        if data is not None:
            self.warning("Receive %s bytes: %r" % (len(data), data))
        else:
            self.warning("Receive nothing")

    def on_session_done(self, score):
        self.error("Done: RX=%s TX=%s" % (
            self.rx_bytes, self.tx_bytes))

    def getScore(self):
        if self.rx_bytes:
            return 1.0
        else:
            return None

