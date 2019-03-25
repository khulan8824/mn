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
	print('data', data)
        connected = self.transport.getPeer().host
        nlist = data.decode('utf-8').split('#')
        for gwInfo in nlist:
            ts, address, latency, sender  = gwInfo.split(',')
            self.client.setGatewayTable(datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"), str(address) ,latency,str(sender))
    	self.client.calculateTrustScore(sender)
            #with open('log%s_%s'%(self.client.myAddress,address),'a') as f:
            #    f.write("{0},{1},{2},{3},{4}\n".format(ts,address,latency, sender, self.transport.getHost().host))
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        return
