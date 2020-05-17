#!/usr/bin/python

"Setting the position of Nodes with wmediumd to calculate the interference"

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import random

def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference,
                       noise_threshold=-91, fading_coefficient=3)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36',
                             position='15,30,0')
    
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid', mode='a', channel='36',
                             position='15,110,0')
    ap3 = net.addAccessPoint('ap3', ssid='new-ssid', mode='a', channel='36',
                             position='115,30,0')
    ap4 = net.addAccessPoint('ap4', ssid='new-ssid', mode='a', channel='36',
                             position='110,110,0')
    
    ap5 = net.addAccessPoint('ap5', ssid='new-ssid', mode='a', channel='36',
                             position='75,75,0')
    
    
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position=str(random.randint(15,40))+','+str(random.randint(0,30))+',10')
    net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8',
                    position=str(random.randint(10,30))+','+str(random.randint(20,50))+',10')
    net.addStation('sta3', ip='10.0.0.3/8',
                   position=str(random.randint(20,40))+','+str(random.randint(10,20))+',10')
    net.addStation('sta4', ip='10.0.0.4/8',                   
                   position=str(random.randint(30,50))+','+str(random.randint(30,45))+',10')
    net.addStation('sta5', ip='10.0.0.5/8',
                   position=str(random.randint(10,20))+','+str(random.randint(20,35))+',10')
    
    net.addStation('sta6', ip='10.0.0.6/8',
                   position=str(random.randint(50,75))+','+str(random.randint(10,50))+',10')
    net.addStation('sta7', ip='10.0.0.7/8',
                   position=str(random.randint(65,85))+','+str(random.randint(30,45))+',10')
    net.addStation('sta8', ip='10.0.0.8/8',
                   position=str(random.randint(85,100))+','+str(random.randint(15,40))+',10')
    net.addStation('sta9', ip='10.0.0.9/8',
                   position=str(random.randint(70,85))+','+str(random.randint(20,45))+',10')
    net.addStation('sta10', ip='10.0.0.10/8',
                   position=str(random.randint(55,65))+','+str(random.randint(40,50))+',10')
    
    
    net.addStation('sta11', ip='10.0.0.11/8',
                   position=str(random.randint(100,120))+','+str(random.randint(5,20))+',10')    
    net.addStation('sta12', ip='10.0.0.12/8',
                   position=str(random.randint(120,145))+','+str(random.randint(15,30))+',10')
    net.addStation('sta13', ip='10.0.0.13/8',
                   position=str(random.randint(115,125))+','+str(random.randint(25,40))+',10')
    net.addStation('sta14', ip='10.0.0.14/8',
                   position=str(random.randint(135,150))+','+str(random.randint(35,45))+',10')
    net.addStation('sta15', ip='10.0.0.15/8',
                   position=str(random.randint(130,145))+','+str(random.randint(40,50))+',10')
    
    
    net.addStation('sta16', ip='10.0.0.16/8',
                   position=str(random.randint(0,20))+','+str(random.randint(50,90))+',10')
    net.addStation('sta17', ip='10.0.0.17/8',
                   position=str(random.randint(5,15))+','+str(random.randint(70,80))+',10')
    net.addStation('sta18', ip='10.0.0.18/8',
                   position=str(random.randint(15,35))+','+str(random.randint(60,80))+',10')
    net.addStation('sta19', ip='10.0.0.19/8',
                   position=str(random.randint(25,40))+','+str(random.randint(75,90))+',10')
    net.addStation('sta20', ip='10.0.0.20/8',
                   position=str(random.randint(35,45))+','+str(random.randint(80,95))+',10')
    
    
    net.addStation('sta21', ip='10.0.0.21/8',
                   position=str(random.randint(55,70))+','+str(random.randint(55,75))+',10')
    net.addStation('sta22', ip='10.0.0.22/8',
                   position=str(random.randint(70,90))+','+str(random.randint(60,80))+',10')
    net.addStation('sta23', ip='10.0.0.23/8',
                   position=str(random.randint(85,99))+','+str(random.randint(70,85))+',10')
    net.addStation('sta24', ip='10.0.0.24/8',
                   position=str(random.randint(50,80))+','+str(random.randint(85,100))+',10')
    net.addStation('sta25', ip='10.0.0.25/8',
                   position=str(random.randint(60,75))+','+str(random.randint(65,85))+',10')
    
    net.addStation('sta26', ip='10.0.0.26/8',
                   position=str(random.randint(110,125))+','+str(random.randint(80,100))+',10')
    net.addStation('sta27', ip='10.0.0.27/8',
                   position=str(random.randint(100,130))+','+str(random.randint(65,85))+',10')
    net.addStation('sta28', ip='10.0.0.28/8',
                   position=str(random.randint(130, 145))+','+str(random.randint(70,95))+',10')
    net.addStation('sta29', ip='10.0.0.29/8',
                   position=str(random.randint(100,120))+','+str(random.randint(55,75))+',10')
    net.addStation('sta30', ip='10.0.0.30/8',
                   position=str(random.randint(130,145))+','+str(random.randint(68,90))+',10')
    
    
    
    info('****Creating gateway nodes***')
    net.addStation('g1', ip='10.0.1.1/8',position='40,40,10', range=300)    
    net.addStation('g2', ip='10.0.1.2/8', position='80,40,0', range=300)    
    net.addStation('g3', ip='10.0.1.3/8',position='120,40,0', range=300)
    
    net.addStation('g4', ip='10.0.1.4/8',position='40,70,0', range=300)    
    net.addStation('g5', ip='10.0.1.5/8',position='80,70,0', range=300)    
    net.addStation('g6', ip='10.0.1.6/8',position='120,70,10', range=300) 
    
    net.addStation('g7', ip='10.0.1.7/8', position='40,120,0', range=300)    
    net.addStation('g8', ip='10.0.1.8/8',position='80,120,0', range=300)    
    net.addStation('g9', ip='10.0.1.9/8',position='120,120,0', range=300) 
    
    net.addStation('g10', ip='10.0.1.10/8',position='75,75,0', range=300)
        
    c1 = net.addController('c1')
       

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=150, max_y=150)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])


    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
