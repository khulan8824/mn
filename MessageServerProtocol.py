import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os

import sys
from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, Protocol
import NeighborManager as neigh
import Gateway as gt

#SERVER SECTION
class MessageServerProtocol(Protocol):
    client = None
    
    def dataReceived(self,data):
        connected = self.transport.getPeer().host
        nlist = data.decode('utf-8').split('#') # received measurements
        self.client.process(connected, nlist)
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        return
