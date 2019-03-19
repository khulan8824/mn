import sys
sys.path.append(".")

import datetime
import time
import os
from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol


import MessageClientProtocol as client
import MessageServerProtocol as server
import NeighborManager as neighbor




nm = neighbor.NeighborManager()

nm.neighborAddress = str(sys.argv[1])

#print("starting...",nm.neighborAddress )

if reactor.running:
    reactor.stop()
    
factory = protocol.ServerFactory()
factory.protocol = server.MessageServerProtocol
reactor.listenTCP(5555, factory)

#print("coming")

#reactor.callLater(5,nm.sendInformation)

#client4.cManager.connectBest()
#time.sleep(10)
nm.send()
#reactor.callInThread(nm.send)

reactor.run()
