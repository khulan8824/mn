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
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4']
        addresses2 = ['10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9']
        addresses3 = ['10.0.0.10', '10.0.0.11', '10.0.0.12', '10.0.0.13']
        
        gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4']
        
        switch = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch1 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s3', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s4', cls=OVSKernelSwitch)

        switch7 = self.addSwitch('s7', cls=OVSKernelSwitch)
        switch8 = self.addSwitch('s8', cls=OVSKernelSwitch)
        switch9 = self.addSwitch('s9', cls=OVSKernelSwitch)
	
        for h in range(len(addresses1)):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)

        for h in range(len(addresses2)):
            host = self.addHost('h%s' % (len(addresses1)+h+1), ip=addresses2[h])
            self.addLink(host, switch2)

        for h in range(len(addresses3)):
            host = self.addHost('h%s' % (len(addresses2)+len(addresses1)+h+1), ip=addresses3[h])
            self.addLink(host, switch3)

        self.addLink(switch7, switch1, delay='2ms')
	self.addLink(switch8, switch2, delay = '2ms')
	self.addLink(switch9, switch3, delay='2ms')
	
	self.addLink(switch, switch7, delay='2ms')
        self.addLink(switch, switch8, delay='2ms')
	self.addLink(switch, switch9, delay='2ms')


        for g in range(len(gwAddresses)):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch, bw=10)
            
            

def simpleTest():
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connection")
    popens = {}
    for h in net.hosts:
	if h.name.startswith('g'):
	    randDelay = random.randint(0,4)
	    #h.cmdPrint("tc qdisc add dev %s-eth0 root netem delay 0ms %dms"%(h.name, randDelay))
	    h.cmdPrint('python -m SimpleHTTPServer 8080 &')
	   
    popens = {}
    for h in net.switches:
        if h.name.startswith('s2'):
	    for n in range(4):
		randDelay = random.randint(2,5)
        	h.cmdPrint("tc qdisc add dev s2-eth%d root netem delay %dms"%(n+1, randDelay))
        if h.name.startswith('s3'):
	    for n in range(4):
		randDelay = random.randint(2,5)
        	h.cmdPrint("tc qdisc add dev s3-eth%d root netem delay %dms"%(n+1, randDelay))
        if h.name.startswith('s4'):
	    for n in range(5):
		randDelay = random.randint(2,5)
        	h.cmdPrint("tc qdisc add dev s4-eth%d root netem delay %dms"%(n+1, randDelay))
	
        if h.name.startswith('s7'):
	    randDelay = random.randint(2,5)
            h.cmdPrint("tc qdisc add dev s2-eth5 root netem delay 5ms")

        if h.name.startswith('s8'):
	    randDelay = random.randint(2,5)
            h.cmdPrint("tc qdisc add dev s3-eth6 root netem delay 5ms")

        if h.name.startswith('s9'):
            h.cmdPrint("tc qdisc add dev s4-eth5 root netem delay 5ms")
	    
	
    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()
