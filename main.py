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


addresses = ['10.139.40.201','10.139.40.202','10.139.40.203','10.139.40.204' ,'10.139.40.205',
             '10.139.40.206','10.139.40.207','10.139.40.208','10.139.40.209','10.139.40.210',
             '10.139.40.211','10.139.40.212','10.139.40.213','10.139.40.214' ,'10.139.40.215',
             '10.139.40.216','10.139.40.217','10.139.40.218','10.139.40.219','10.139.40.220']

gwAddresses = ['10.139.40.85', '10.139.40.122', '10.138.57.2', '10.138.85.130', 
               '10.139.37.194', '10.138.25.67', '10.138.29.98', '10.228.192.210', '10.228.193.210',
              '10.228.204.9','10.145.32.66']

nm = neighbor.NeighborManager()

nm.myAddress = str(sys.argv[1])
nm.neighbors = addresses
nm.gateways = gwAddresses
nm.trshld = 10
nm.period = 120
nm.sampleSize = 3


if reactor.running:
    reactor.stop()
    
factory = protocol.ServerFactory()
factory.protocol = server.MessageServerProtocol
factory.protocol.client = nm
reactor.listenTCP(5555, factory)


reactor.callLater(5,nm.senseNeighbors)
reactor.callLater(15, nm.send)
#reactor.callLater(15, nm.senseBest)
reactor.callLater(nm.period, nm.download)

reactor.run()
