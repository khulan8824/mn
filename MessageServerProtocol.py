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
        print('data:', data)
        
        #self.transport.write("connected")
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        return
