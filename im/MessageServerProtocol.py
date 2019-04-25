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

#SERVER SECTION
class MessageServerProtocol(Protocol):
    client = None
    
    def dataReceived(self,data):
	#print('data', data)
        connected = self.transport.getPeer().host
        print("connected", connected)
        nlist = data.decode('utf-8').split('#')
        for gwInfo in nlist:
            ts, address, latency, sender  = gwInfo.split(',')
            self.client.setGatewayTable(datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"), str(address.encode('ascii', 'ignore')) ,float(latency.encode('ascii', 'ignore')),str(sender.encode('ascii', 'ignore')))
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        return