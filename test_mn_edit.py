#!/usr/bin/python

from mininet.node import Host
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from subprocess import call

def myNetwork():

    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    
    c0 = net.addController('c0')
    
    info( '*** Add switches/APs\n')
    ap4 = net.addAccessPoint('ap4', cls=OVSKernelAP, ssid='ap4-ssid',
                             channel='1', mode='g', ip='', position='721.0,500.0,0', range=1000)
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid',
                             channel='1', mode='g', position='334.0,387.0,0')

    info( '*** Add hosts/stations\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1', position='321.0,170.0,0')
    sta7 = net.addStation('sta7', ip='10.0.0.7',position='333.0,611.0,0')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.11', defaultRoute=None)
    sta3 = net.addStation('sta3', ip='10.0.0.3', position='542.0,538.0,0')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    sta10 = net.addStation('sta10', ip='10.0.0.10',
                           position='198.0,197.0,0')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    sta4 = net.addStation('sta4', ip='10.0.0.4',
                           position='161.0,552.0,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2',
                           position='539.0,209.0,0')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    sta5 = net.addStation('sta5', ip='10.0.0.5',
                           position='602.0,337.0,0')
    sta9 = net.addStation('sta9', ip='10.0.0.9',
                           position='117.0,287.0,0')
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    sta6 = net.addStation('sta6', ip='10.0.0.6',
                           position='102.0,411.0,0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    
    net.addLink(sta1,ap1)
    net.addLink(sta10,ap1)
    net.addLink(sta9, ap1)
    net.addLink(sta6, ap1)
    net.addLink(sta4, ap1)
    net.addLink(sta7, ap1)
    net.addLink(sta3, ap1)
    net.addLink(sta5,ap1)
    net.addLink(sta2,ap1)
    net.addLink(ap1, cls=mesh, ssid='new-ssid', mode='g', channel=1)
    
    net.addLink(h1, ap4)
    net.addLink(h2, ap4)
    net.addLink(h10, ap4)
    net.addLink(h4, ap4)
    net.addLink(h5, ap4)
    net.addLink(h6, ap4)
    net.addLink(h7, ap4)
    net.addLink(h8, ap4)
    net.addLink(h9, ap4)
    net.addLink(h3, ap4)
    
    net.addLink(ap4, cls=mesh, ssid='new-ssid', mode='g', channel=1)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap4').start([c0])
    net.get('ap1').start([c0])

    info( '*** Post configure nodes\n')

    CLI_wifi(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

