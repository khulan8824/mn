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


addresses = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4']
gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4']
nm = neighbor.NeighborManager()

nm.myAddress = str(sys.argv[1])
nm.neighbors = addresses
nm.gateways = gwAddresses
nm.trshld = 10


if reactor.running:
    reactor.stop()
    
factory = protocol.ServerFactory()
factory.protocol = server.MessageServerProtocol
factory.protocol.client = nm
reactor.listenTCP(5555, factory)


reactor.callLater(5,nm.senseNeighbors)
reactor.callLater(15, nm.send)

reactor.run()
