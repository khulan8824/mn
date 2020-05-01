#!/usr/bin/python

'This example shows how to create wireless link between two APs'

from mininet.node import Controller, Host
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
    
    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1,', position='25,25,0')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid2,', position='50,50,0')
    ap3 = net.addAccessPoint('ap3', wlans=2, ssid='ssid3,', position='75,75,0')    
    ap4 = net.addAccessPoint('ap4', wlans=2, ssid='ssid4,', position='75,75,0')    
    
    #Gateway APs
    ap5 = net.addAccessPoint('ap5', wlans=2, ssid='ssid5,', position='40,40,0')
    ap6 = net.addAccessPoint('ap6', wlans=2, ssid='ssid6,', position='80,40,0')    
    ap7 = net.addAccessPoint('ap7', wlans=2, ssid='ssid6,', position='50,60,0')
    
    
    nodes1 = []
    nodes2 = []
    nodes3 = []
    nodes4 = []
    nodes5 = []
    
    c0 = net.addController('c0')
    i =1
    
    
    sta1 = net.addStation('sta1', position='0,0,0')    
    sta2 = net.addStation('sta2', position='15,15,0')
    sta3 = net.addStation('sta3', position='25,10,0')
    sta4 = net.addStation('sta4', position='25,30,0')
    sta5 = net.addStation('sta5', position='45,5,0')
    sta6 = net.addStation('sta6', position='45,25,0')
    sta7 = net.addStation('sta7', position='37,18,0')
    sta8 = net.addStation('sta8', position='37,48,0')
    sta9 = net.addStation('sta9', position='10,25,0')
    sta10 = net.addStation('sta10', position='10,45,0')
    
    
    nodes1.append(sta1)
    nodes1.append(sta2)
    nodes1.append(sta3)
    nodes1.append(sta4)
    nodes1.append(sta5)
    nodes1.append(sta6)
    nodes1.append(sta7)
    nodes1.append(sta8)
    nodes1.append(sta9)
    nodes1.append(sta10)
    
    
    sta11 = net.addStation('sta11', position='50,0,0')    
    sta12 = net.addStation('sta12', position='55,15,0')
    sta13 = net.addStation('sta13', position='75,10,0')
    sta14 = net.addStation('sta14', position='75,30,0')
    sta15 = net.addStation('sta15', position='95,5,0')
    sta16 = net.addStation('sta16', position='95,25,0')
    sta17 = net.addStation('sta17', position='87,18,0')
    sta18 = net.addStation('sta18', position='87,48,0')
    sta19 = net.addStation('sta19', position='60,25,0')
    sta20 = net.addStation('sta20', position='60,45,0')
    nodes2.append(sta11)
    nodes2.append(sta12)
    nodes2.append(sta13)
    nodes2.append(sta14)
    nodes2.append(sta15)
    nodes2.append(sta16)
    nodes2.append(sta17)
    nodes2.append(sta18)
    nodes2.append(sta19)
    nodes2.append(sta20)
    
    
    sta21 = net.addStation('sta21', position='0,50,0')    
    sta22 = net.addStation('sta22', position='15,65,0')
    sta23 = net.addStation('sta23', position='25,60,0')
    sta24 = net.addStation('sta24', position='25,80,0')
    sta25 = net.addStation('sta25', position='45,55,0')
    sta26 = net.addStation('sta26', position='45,75,0')
    sta27 = net.addStation('sta27', position='37,68,0')
    sta28 = net.addStation('sta28', position='37,98,0')
    sta29 = net.addStation('sta29', position='10,75,0')
    sta30 = net.addStation('sta30', position='10,95,0')
    nodes3.append(sta21)
    nodes3.append(sta22)
    nodes3.append(sta23)
    nodes3.append(sta24)
    nodes3.append(sta25)
    nodes3.append(sta26)
    nodes3.append(sta27)
    nodes3.append(sta28)
    nodes3.append(sta29)
    nodes3.append(sta30)
    
    
    sta31 = net.addStation('sta31', position='50,50,0')    
    sta32 = net.addStation('sta32', position='55,65,0')
    sta33 = net.addStation('sta33', position='75,60,0')
    sta34 = net.addStation('sta34', position='75,80,0')
    sta35 = net.addStation('sta35', position='95,55,0')
    sta36 = net.addStation('sta36', position='95,75,0')
    sta37 = net.addStation('sta37', position='87,68,0')
    sta38 = net.addStation('sta38', position='87,98,0')
    sta39 = net.addStation('sta39', position='60,75,0')
    sta40 = net.addStation('sta40', position='60,95,0')
    nodes4.append(sta31)
    nodes4.append(sta32)
    nodes4.append(sta33)
    nodes4.append(sta34)
    nodes4.append(sta35)
    nodes4.append(sta36)
    nodes4.append(sta37)
    nodes4.append(sta38)
    nodes4.append(sta39)
    nodes4.append(sta40)
    
    
    
    g1 = net.addHost('g1', cls=Host, position='15,15,0')  #ap5    
    g2 = net.addHost('g2', cls=Host, position='35,35,0') #ap5
    g3 = net.addHost('g3', cls=Host, position='55,55,0') #ap6
    g4 = net.addHost('g4', cls=Host, position='75,75,0') #ap7
    g5 = net.addHost('g5', cls=Host, position='85,15,0') #ap6
    g6 = net.addHost('g6', cls=Host, position='65,35,0') #ap6
    g7 = net.addHost('g7', cls=Host, position='45,55,0') #ap5
    g8 = net.addHost('g8', cls=Host, position='25,75,0')  #ap7
    g9 = net.addHost('g9', cls=Host, position='50,50,0') #ap5
    g10 = net.addHost('g10', cls=Host, position='75,25,0')#ap6
    
    net.addLink(g1, ap5)
    net.addLink(g2, ap5)
    net.addLink(g3, ap6)
    net.addLink(g4, ap7)
    net.addLink(g5, ap6)
    net.addLink(g6, ap6)
    net.addLink(g7, ap5)
    net.addLink(g8, ap7)
    net.addLink(g9, ap5)
    net.addLink(g10, ap6)
    
        
    
    net.plotGraph(max_x=100, max_y=100)    
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    #net.setMobilityModel(time=0, model='RandomDirection', max_x=150, max_y=150)
    
    info("*** Associating Stations\n")
    for node in nodes1:
        net.addLink(node, ap1)
        
    for node in nodes2:        
        net.addLink(node, ap2)
        
    for node in nodes3:        
        net.addLink(node, ap3)
                
    for node in nodes4:        
        net.addLink(node, ap4)
        
    #for node in nodes5:        
    #    net.addLink(node, ap5)
        
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap4, intf='ap4-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap5, intf='ap5-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap6, intf='ap6-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap7, intf='ap7-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Starting network\n")
    net.build()


    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    ap4.start([c0])
    ap5.start([c0])
    ap6.start([c0])
    ap7.start([c0])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
