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

#SERVER SECTION
class MessageServerProtocol(Protocol):

    def dataReceived(self,data):
        connected = self.transport.getPeer().host
        #print('Client:', connected)
        #print('data:', data)
        nlist = data.decode('utf-8').split('#')
        for gwInfo in nlist:
            ts, address, latency, sender  = gwInfo.split(',')
            with open('log','a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(ts,address,latency, sender, self.transport.getHost().host))
        #self.transport.write("connected")
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        return
