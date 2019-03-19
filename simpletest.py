from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

class SingleSwitchTopo(Topo):
    "Single switch connected to n hostst"
    def build(self, n=2):
        addresses = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4']
        gwAddresses = ['10.0.0.10', '10.0.0.11', '10.0.0.12', '10.0.0.13']
        switch = self.addSwitch('s1')
        for h in range(4):
            host = self.addHost('h%s' % (h+1), ip=addresses[h])
            self.addLink(host, switch)
        for g in range(2):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch)

def simpleTest():
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connection")
    #
    for h in net.hosts:
        if h.name.startswith('g'):
            h.sendCmd("python -m SimpleHTTPServer 8080 &")
    #CLI(net)
    
    for h in net.hosts:
        if h.name.startswith('h'):
            h.sendCmd("python main.py "+h.IP())
    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()
