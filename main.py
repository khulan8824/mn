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


addresses = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9', '10.0.0.10',
             '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14', '10.0.0.15', '10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20',
             '10.0.0.21', '10.0.0.22', '10.0.0.23', '10.0.0.24', '10.0.0.25', '10.0.0.26', '10.0.0.27', '10.0.0.28', '10.0.0.29', '10.0.0.30',
             '10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36', '10.0.0.37', '10.0.0.38', '10.0.0.39', '10.0.0.40', 
             '10.0.0.41', '10.0.0.42', '10.0.0.43', '10.0.0.44', '10.0.0.45', '10.0.0.46', '10.0.0.47', '10.0.0.48', 
             '10.0.0.49', '10.0.0.50',
             '10.0.0.51', '10.0.0.52', '10.0.0.53', '10.0.0.54', '10.0.0.55', '10.0.0.56', '10.0.0.57', '10.0.0.58', '10.0.0.59', '10.0.0.60']#,
             #'10.0.0.61', '10.0.0.62', '10.0.0.63', '10.0.0.64', '10.0.0.65', '10.0.0.66', '10.0.0.67', '10.0.0.68', '10.0.0.69', '10.0.0.70',
             #'10.0.0.71', '10.0.0.72', '10.0.0.73', '10.0.0.74', '10.0.0.75', '10.0.0.76', '10.0.0.77', '10.0.0.78', '10.0.0.79', '10.0.0.80', 
             #'10.0.0.81', '10.0.0.82', '10.0.0.83', '10.0.0.84', '10.0.0.85', '10.0.0.86', '10.0.0.87', '10.0.0.88', '10.0.0.89', '10.0.0.90']
gwAddresses = [#'10.0.0.85', '10.0.0.86', '10.0.0.87', '10.0.0.88', '10.0.0.89', '10.0.0.90',
    '10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5',
    '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']
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
