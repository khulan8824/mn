from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

class SingleSwitchTopo(Topo):
    "Single switch connected to n hostst"
    def build(self, n=2):
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.6','10.0.0.7', 
                     '10.0.0.8', '10.0.0.9', '10.0.0.10', '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14', '10.0.0.15']
        addresses2 = ['10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20', '10.0.0.21','10.0.0.22', 
                     '10.0.0.23', '10.0.0.24', '10.0.0.25']
        gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4']
        
        switch = self.addSwitch('s1')
        switch1 = self.addSwitch('s2')
        switch2 = self.addSwitch('s3')
        for h in range(15):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)
        
        for h in range(10):
            host = self.addHost('h%s'% (h+len(addresses1)+1), ip=addresses2[h])
            self.addLink(host, switch2)
        
        for g in range(4):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch)
            
            
        #self.addLink(switch, switch1)
        #self.addLink(switch, switch2)

def simpleTest():
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connection")
    #
    for h in net.hosts:
        if h.name.startswith('g'):
            h.sendCmd("python -m SimpleHTTPServer 8080 &")
            
    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()
