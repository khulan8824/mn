#!/usr/bin/python

from mininet.node import Controller, Host
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
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info( '*** Add switches/APs\n')
    ap3 = net.addAccessPoint('ap3', cls=OVSKernelAP, ssid='ap3-ssid',
                             channel='1', mode='g', position='1196.0,769.0,0')
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid',
                             channel='1', mode='g', position='527.0,256.0,0')
    ap4 = net.addAccessPoint('ap4', cls=OVSKernelAP, ssid='ap4-ssid',
                             channel='1', mode='g', position='1395.0,523.0,0')
    ap2 = net.addAccessPoint('ap2', cls=OVSKernelAP, ssid='ap2-ssid',
                             channel='1', mode='g', ip='', position='871.0,346.0,0', range=600)

    info( '*** Add hosts/stations\n')
    sta25 = net.addStation('sta25', ip='10.0.0.28',
                           position='1345.0,660.0,0')
    sta11 = net.addStation('sta11', ip='10.0.0.23',
                           position='1033.0,812.0,0')
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='372.0,71.0,0')
    sta21 = net.addStation('sta21', ip='10.0.0.21',
                           position='1193.0,458.0,0')
    sta19 = net.addStation('sta19', ip='10.0.0.19',
                           position='1175.0,953.0,0')
    sta29 = net.addStation('sta29', ip='10.0.0.29',
                           position='1526.0,318.0,0')
    sta17 = net.addStation('sta17', ip='10.0.0.17',
                           position='1471.0,807.0,0')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    sta9 = net.addStation('sta9', ip='10.0.0.9',
                           position='316.0,187.0,0')
    sta8 = net.addStation('sta8', ip='10.0.0.8',
                           position='298.0,316.0,0')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    sta15 = net.addStation('sta15', ip='10.0.0.15',
                           position='1273.0,546.0,0')
    sta23 = net.addStation('sta23', ip='10.0.0.23',
                           position='1409.0,413.0,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2',
                           position='562.0,60.0,0')
    sta5 = net.addStation('sta5', ip='10.0.0.5',
                           position='705.0,368.0,0')
    sta22 = net.addStation('sta22', ip='10.0.0.25',
                           position='58.0,-40.0,0')
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    sta30 = net.addStation('sta30', ip='10.0.0.30',
                           position='1268.0,413.0,0')
    sta6 = net.addStation('sta6', ip='10.0.0.6',
                           position='560.0,468.0,0')
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    sta14 = net.addStation('sta14', ip='10.0.0.14',
                           position='1141.0,583.0,0')
    sta26 = net.addStation('sta26', ip='10.0.0.26',
                           position='1523.0,633.0,0')
    sta10 = net.addStation('sta10', ip='10.0.0.10',
                           position='474.0,136.0,0')
    sta20 = net.addStation('sta20', ip='10.0.0.20',
                           position='1026.0,913.0,0')
    sta12 = net.addStation('sta12', ip='10.0.0.12',
                           position='979.0,727.0,0')
    sta24 = net.addStation('sta24', ip='10.0.0.24',
                           position='1233.0,636.0,0')
    sta22 = net.addStation('sta22', ip='10.0.0.25',
                           position='1282.0,278.0,0')
    sta28 = net.addStation('sta28', ip='10.0.0.31',
                           position='1620.0,398.0,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3',
                           position='727.0,105.0,0')
    sta7 = net.addStation('sta7', ip='10.0.0.7',
                           position='379.0,434.0,0')
    sta16 = net.addStation('sta16', ip='10.0.0.16',
                           position='1424.0,680.0,0')
    sta13 = net.addStation('sta13', ip='10.0.0.13',
                           position='1044.0,619.0,0')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    sta18 = net.addStation('sta18', ip='10.0.0.18',
                           position='1356.0,950.0,0')
    sta27 = net.addStation('sta27', ip='10.0.0.27',
                           position='1642.0,524.0,0')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6')
    sta4 = net.addStation('sta4', ip='10.0.0.4',  position='781.0,266.0,0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(sta27, ap4)
    net.addLink(sta28, ap4)
    net.addLink(sta23, ap4)
    net.addLink(sta29, ap4)
    net.addLink(sta22, ap4)
    net.addLink(ap2, cls=mesh, ssid='new-ssid', mode='g', channel=1)
    net.addLink(ap3, cls=mesh, ssid='new-ssid', mode='g', channel=1)
    net.addLink(ap4, cls=mesh, ssid='new-ssid', mode='g', channel=1)
    net.addLink(ap1, cls=mesh, ssid='new-ssid', mode='g', channel=1)
    net.addLink(sta10, ap1)
    net.addLink(sta2, ap1)
    net.addLink(sta3, ap1)
    net.addLink(sta1, ap1)
    net.addLink(sta9, ap1)
    net.addLink(sta8, ap1)
    net.addLink(sta7, ap1)
    net.addLink(sta6, ap1)
    net.addLink(sta5, ap1)
    net.addLink(sta4, ap1)
    net.addLink(h10, ap2)
    net.addLink(h4, ap2)
    net.addLink(h5, ap2)
    net.addLink(h7, ap2)
    net.addLink(h1, ap2)
    net.addLink(h8, ap2)
    net.addLink(h2, ap2)
    net.addLink(h9, ap2)
    net.addLink(h3, ap2)
    net.addLink(h6, ap2)
    net.addLink(sta11, ap3)
    net.addLink(sta12, ap3)
    net.addLink(sta13, ap3)
    net.addLink(sta14, ap3)
    net.addLink(sta15, ap3)
    net.addLink(sta16, ap3)
    net.addLink(sta17, ap3)
    net.addLink(sta18, ap3)
    net.addLink(sta19, ap3)
    net.addLink(sta20, ap3)
    net.addLink(sta30, ap4)
    net.addLink(sta21, ap4)
    net.addLink(sta24, ap4)
    net.addLink(sta25, ap4)
    net.addLink(sta26, ap4)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap3').start([c0])
    net.get('ap1').start([c0])
    net.get('ap4').start([c0])
    net.get('ap2').start([c0])

    info( '*** Post configure nodes\n')

    CLI_wifi(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

