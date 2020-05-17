#!/usr/bin/python

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import random

def topology(autoTxPower):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    

    info("*** Creating nodes\n")    
    i = 1
    nodes = []
    while i<50:        
        sta = net.addStation('sta'+str(i), position=str(random.randint(20,130))+','+str(random.randint(20,130))+',0')
        nodes.append(sta)
        i+=1
    net.setPropagationModel(model="logDistance", exp=4)
    net.plotGraph(max_x=150, max_y=150)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    
    i =1
    for node in nodes:        
        net.addLink(node, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
        i+=1
    info("*** Starting network\n")
    net.build()

    #i =1
    #for node in nodes:        
    #    sta.setIPv6('2001::'+str(i)+'/64', intf="sta"+str(i)+"-wlan0")
    #    i+=1
        
        
    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    autoTxPower = True if '-a' in sys.argv else False
    topology(autoTxPower)
