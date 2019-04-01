from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, UserSwitch  
import random

class SingleSwitchTopo(Topo):
    "Single switch connected to n hostst"
    def build(self, n=2):
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.6','10.0.0.7', 
                     '10.0.0.8', '10.0.0.9', '10.0.0.10', '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14', '10.0.0.15']
        addresses2 = ['10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20', '10.0.0.21','10.0.0.22', 
                     '10.0.0.23', '10.0.0.24', '10.0.0.25', '10.0.0.26','10.0.0.27', '10.0.0.28', '10.0.0.29', '10.0.0.30']

        addresses3 = ['10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36','10.0.0.37', 
                     '10.0.0.38', '10.0.0.39', '10.0.0.40', '10.0.0.41','10.0.0.42', '10.0.0.43', '10.0.0.44', '10.0.0.45', '10.0.0.46', '10.0.0.47'
		     , '10.0.0.48', '10.0.0.49', '10.0.0.50', '10.0.0.51', '10.0.0.52', '10.0.0.53', '10.0.0.54', '10.0.0.55', '10.0.0.56', '10.0.0.57', '10.0.0.58', '10.0.0.59', '10.0.0.60']
        gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5', '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']
        
        switch = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch1 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s3', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s4', cls=OVSKernelSwitch)
	
        for h in range(15):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)
        
        for h in range(15):
            host = self.addHost('h%s'% (h+len(addresses1)+1), ip=addresses2[h])
            self.addLink(host, switch2)
        
        for h in range(30):
            host = self.addHost('h%s'% (h+len(addresses1)+len(addresses2)+1), ip=addresses3[h])
            self.addLink(host, switch3)
        
        self.addLink(switch, switch1)
        self.addLink(switch, switch2)
        self.addLink(switch, switch3)
        
        for g in range(10):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch, bw=10)
            
            

def simpleTest():
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connection")
    popens = {}
    #for h in net.hosts:
	#if h.name.startswith('g'):
	    #h.cmdPrint('python -m SimpleHTTPServer 8080 &')
    CLI(net)
    for h in net.hosts:
        if h.name.startswith('h'):
	    randDelay = random.randint(0,15)
            h.cmdPrint("tc qdisc add dev %s-eth0 root netem delay %dms"%(h.name, randDelay))
	    h.cmdPrint('python sense.py %s &'%(h.IP()))
	    
	
    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()
