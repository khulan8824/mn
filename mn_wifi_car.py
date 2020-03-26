#!/usr/bin/python

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import UserAP

import random

def topology():
    addresses = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9', '10.0.0.10']#,
            #    '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14', '10.0.0.15', '10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20',
            #   '10.0.0.21', '10.0.0.22', '10.0.0.23', '10.0.0.24', '10.0.0.25', '10.0.0.26', '10.0.0.27', '10.0.0.28', '10.0.0.29', '10.0.0.30',
             #  '10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36', '10.0.0.37', '10.0.0.38', '10.0.0.39', '10.0.0.40',
              # '10.0.0.41', '10.0.0.42', '10.0.0.43', '10.0.0.44', '10.0.0.45', '10.0.0.46', '10.0.0.47', '10.0.0.48', '10.0.0.49', '10.0.0.50',
               #'10.0.0.51', '10.0.0.52', '10.0.0.53', '10.0.0.54', '10.0.0.55', '10.0.0.56', '10.0.0.57', '10.0.0.58', '10.0.0.59', '10.0.0.60']
    
    gateways = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5', '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    info("*** Creating Nodes\n")
    nodes = []
    gws = [] 
    cnt =1 
    c1 = net.addController('c1')
    c1.start()
            
    for gw in gateways:
        gw = net.addStation('gw'+str(cnt), ip=gw+"/8", position=str(random.randint(0,300))+','+str(random.randint(0,300))+','+str(random.randint(0,300)))
        gws.append(gw)
        cnt+=1
    
    
    cnt = 1
    for addr in addresses:
        sta = net.addStation('n'+str(cnt), ip=addr+"/8", position=str(random.randint(0,300))+','+str(random.randint(0,300))+','+str(random.randint(0,300)))
        nodes.append(sta)
        cnt+=1
        
    net.setPropagationModel(model="logDistance", exp=3.5)
    
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()    
    
    info("*** Creating links\n")
    for gw in gws:
        net.addLink(gw, cls=mesh, ssid='meshNet', channel=5, ht_cap='HT40+')
    
    
    for node in nodes:
        net.addLink(node, cls=mesh, ssid='meshNet', channel=5, ht_cap='HT40+')
        
    net.plotGraph(max_x=300, max_y=300)
    #net.startMobility(time=0, model='RandomDirection', max_x=300, max_y=300, min_v=0.5, max_v=0.8, seed=20)
    
    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()
   
    
if __name__ == "__main__":
    setLogLevel("info")
    topology()