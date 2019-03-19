
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
from twisted.internet.protocol import ClientFactory, Protocol

#CLIENT SECTION
class MessageClientProtocol(Protocol):    
    addr = ""
    status = False
    text = "From inside"
    mode = "client"
    
    def connectionMade(self):
        print("sending info")
        self.transport.write(self.text.encode())
	#self.sense()
        self.transport.loseConnection()
            
    def dataReceived(self,data):
        print('Data received at client side:>', data)
        #self.transport.write(self.text.encode())

    def connectionLost(self, reason):
	return
	#print('Connection lost')

    def sense(self):
	self.text = "sensing info"
	self.transport.write(self.text.encode())
	reactor.callLater(60, self.sense)
