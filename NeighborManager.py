import random
import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os

import sys
from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

import MessageServerProtocol as server
import MessageClientProtocol as client

class NeighborManager:
    neighborAddress= ""
    
    #def sendInformation(self):
    #    f = protocol.ClientFactory()
    #    f.protocol = client.MessageClientProtocol
    #    f.protocol.addr = self.neighborAddress
    #    f.protocol.text = "Welcome"
    #    reactor.connectTCP(self.neighborAddress, 5555, f)
    #    print('sending')
        
    def sense(self):
        f = protocol.ClientFactory()
        f.protocol = client.MessageClientProtocol        
        f.protocol.addr = self.neighborAddress
        f.protocol.text = "Hello world"
        reactor.connectTCP(self.neighborAddress, 5555, f)
	if not reactor.running:	
	    reactor.run()
        
    def send(self):
        reactor.callLater(60, self.send)
        self.sense()
