#!/usr/bin/python

'This example shows how to create wireless link between two APs'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import random


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    
    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1,', position='30,30,0')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid2,', position='70,70,0')
    ap3 = net.addAccessPoint('ap3', wlans=2, ssid='ssid3,', position='50,50,0')
    ap4 = net.addAccessPoint('ap4', wlans=2, ssid='ssid4,', position='100,50,0')
    ap5 = net.addAccessPoint('ap5', wlans=2, ssid='ssid2,', position='120,80,0')
    
    nodes1 = []
    nodes2 = []
    nodes3 = []
    nodes4 = []
    nodes5 = []
    
    c0 = net.addController('c0')
    i =1
    while i<11:
        #sta = net.addStation('sta'+str(i), position=str(random.randint(20,130))+','+str(random.randint(20,130))+',0')
        sta = net.addStation('sta'+str(i))
        nodes1.append(sta)
        i+=1
    
    
    i =11
    while i<21:
        #sta = net.addStation('sta'+str(i), position=str(random.randint(20,130))+','+str(random.randint(20,130))+',0', range=100)
        sta = net.addStation('sta'+str(i))
        nodes2.append(sta)
        i+=1
    
    i =21
    while i<31:
        #sta = net.addStation('sta'+str(i), position=str(random.randint(20,130))+','+str(random.randint(20,130))+',0', range=100)
        sta = net.addStation('sta'+str(i))
        nodes3.append(sta)
        i+=1
        
    i =31
    while i<41:
        #sta = net.addStation('sta'+str(i), position=str(random.randint(20,130))+','+str(random.randint(20,130))+',0', range=100)
        sta = net.addStation('sta'+str(i))
        nodes4.append(sta)
        i+=1
        
    i =41
    while i<51:
        sta = net.addStation('gw'+str(i), position=str(random.randint(20,130))+','+str(random.randint(20,130))+',0', range=100) 
        nodes5.append(sta)
        i+=1
        
    
    #net.plotGraph(max_x=150, max_y=150)    
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.setMobilityModel(time=0, model='RandomDirection', max_x=150, max_y=150)
    
    info("*** Associating Stations\n")
    for node in nodes1:
        net.addLink(node, ap1)
        
    for node in nodes2:        
        net.addLink(node, ap2)
        
    for node in nodes3:        
        net.addLink(node, ap3)
                
    for node in nodes4:        
        net.addLink(node, ap4)
        
    for node in nodes5:        
        net.addLink(node, ap5)
        
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap4, intf='ap4-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap5, intf='ap5-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Starting network\n")
    net.build()

    #for node in nodes5:
#	node.cmd('python -m SimpleHTTPServer 8080 &')
#    for node in nodes1:
#	node.cmd('python main.py '+node.params['ip'][0][:-2]+' &')
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    ap4.start([c0])
    ap5.start([c0])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
