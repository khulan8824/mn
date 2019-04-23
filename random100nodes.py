from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, UserSwitch  
from mininet.node import RemoteController, OVSSwitch

import random

class MultiSwitchTopo(Topo):
    "multiple switch connected to n hostst"
    def build(self):
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4','10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9','10.0.0.10']
        addresses2 = ['10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14','10.0.0.15','10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20']
        addresses3 = ['10.0.0.21', '10.0.0.22', '10.0.0.23', '10.0.0.24','10.0.0.25','10.0.0.26', '10.0.0.27', '10.0.0.28', '10.0.0.29', '10.0.0.30']
        addresses4 = ['10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34','10.0.0.35','10.0.0.36', '10.0.0.37', '10.0.0.38', '10.0.0.39', '10.0.0.40']
        addresses5 = ['10.0.0.41', '10.0.0.42', '10.0.0.43', '10.0.0.44','10.0.0.45','10.0.0.46', '10.0.0.47', '10.0.0.48', '10.0.0.49', '10.0.0.50']
        addresses6 = ['10.0.0.51', '10.0.0.52', '10.0.0.53', '10.0.0.54','10.0.0.55','10.0.0.56', '10.0.0.57', '10.0.0.58', '10.0.0.59', '10.0.0.60']
        addresses7 = ['10.0.0.61', '10.0.0.62', '10.0.0.63', '10.0.0.64','10.0.0.65','10.0.0.66', '10.0.0.67', '10.0.0.68', '10.0.0.69', '10.0.0.70']
        addresses8 = ['10.0.0.71', '10.0.0.72', '10.0.0.73', '10.0.0.74','10.0.0.75','10.0.0.76', '10.0.0.77', '10.0.0.78', '10.0.0.79', '10.0.0.80']
        #addresses9 = ['10.0.0.81', '10.0.0.82', '10.0.0.83', '10.0.0.84','10.0.0.85','10.0.0.86', '10.0.0.87', '10.0.0.88', '10.0.0.89', '10.0.0.90']
        #addresses10 = ['10.0.0.91', '10.0.0.92', '10.0.0.93', '10.0.0.94','10.0.0.95','10.0.0.96', '10.0.0.97', '10.0.0.98', '10.0.0.99', '10.0.0.100']
        
        gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5', '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']
        
        switch = self.addSwitch('s21', cls=OVSKernelSwitch)

        switch1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s3', cls=OVSKernelSwitch)
	switch4 = self.addSwitch('s4', cls=OVSKernelSwitch)
	switch5 = self.addSwitch('s5', cls=OVSKernelSwitch)
	switch6 = self.addSwitch('s6', cls=OVSKernelSwitch)
        switch7 = self.addSwitch('s7', cls=OVSKernelSwitch)
        switch8 = self.addSwitch('s8', cls=OVSKernelSwitch)
        #switch9 = self.addSwitch('s9', cls=OVSKernelSwitch)
        #switch10 = self.addSwitch('s10', cls=OVSKernelSwitch)


        switch11 = self.addSwitch('s11', cls=OVSKernelSwitch)
        switch12 = self.addSwitch('s12', cls=OVSKernelSwitch)
        switch13 = self.addSwitch('s13', cls=OVSKernelSwitch)
        switch14 = self.addSwitch('s14', cls=OVSKernelSwitch)
        switch15 = self.addSwitch('s15', cls=OVSKernelSwitch)
        switch16 = self.addSwitch('s16', cls=OVSKernelSwitch)
        switch17 = self.addSwitch('s17', cls=OVSKernelSwitch)
        switch18 = self.addSwitch('s18', cls=OVSKernelSwitch)
        #switch19 = self.addSwitch('s19', cls=OVSKernelSwitch)
        #switch20 = self.addSwitch('s20', cls=OVSKernelSwitch)
	
        for h in range(len(addresses1)):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)

        for h in range(len(addresses2)):
            host = self.addHost('h%s' % (len(addresses1)+h+1), ip=addresses2[h])
            self.addLink(host, switch2)

        for h in range(len(addresses3)):
            host = self.addHost('h%s' % (len(addresses2)+len(addresses1)+h+1), ip=addresses3[h])
            self.addLink(host, switch3)
	
        for h in range(len(addresses4)):
            host = self.addHost('h%s' % (len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses4[h])
            self.addLink(host, switch4)
	
        for h in range(len(addresses5)):
            host = self.addHost('h%s' % (len(addresses4)+len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses5[h])
            self.addLink(host, switch5)

        for h in range(len(addresses6)):
            host = self.addHost('h%s' % (len(addresses5)+len(addresses4)+len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses6[h])
            self.addLink(host, switch6)

        for h in range(len(addresses7)):
            host = self.addHost('h%s' % (len(addresses6)+len(addresses5)+len(addresses4)+len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses7[h])
            self.addLink(host, switch7)

        for h in range(len(addresses8)):
            host = self.addHost('h%s' % (len(addresses7)+len(addresses6)+len(addresses5)+len(addresses4)+len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses8[h])
            self.addLink(host, switch8)

        #for h in range(len(addresses9)):
        #    host = self.addHost('h%s' % (len(addresses8)+len(addresses7)+len(addresses6)+len(addresses5)+len(addresses4)+len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses9[h])
        #    self.addLink(host, switch9)

        #for h in range(len(addresses10)):
        #    host = self.addHost('h%s' % (len(addresses9)+len(addresses8)+len(addresses7)+len(addresses6)+len(addresses5)+len(addresses4)+len(addresses3)+len(addresses2)+len(addresses1)+h+1), ip=addresses10[h])
        #    self.addLink(host, switch10)


        for g in range(len(gwAddresses)):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch)

        self.addLink(switch11, switch1)
	self.addLink(switch12, switch2)
	self.addLink(switch13, switch3)
	self.addLink(switch14, switch4)	
	self.addLink(switch15, switch5)
	self.addLink(switch16, switch6)
	self.addLink(switch17, switch7)
	self.addLink(switch18, switch8)	
	#self.addLink(switch19, switch9)
	#self.addLink(switch20, switch10)
	
	self.addLink(switch, switch11)
        self.addLink(switch, switch12)
	self.addLink(switch, switch13)
	self.addLink(switch, switch14)
	self.addLink(switch, switch15)
	self.addLink(switch, switch16)
	self.addLink(switch, switch17)
	self.addLink(switch, switch18)
	#self.addLink(switch, switch19)
	#self.addLink(switch, switch20)

            
            

def simpleTest():
    topo = MultiSwitchTopo()
    net = Mininet(topo = topo, switch = OVSSwitch, controller= lambda name: RemoteController(name, ip= '127.0.0.1'))
    net.start()
    print("Dumping host connection")
	   
    popens = {}
    for h in net.switches:

        if h.name=='s1':
	    for n in range(10):
		randDelay = random.randint(1,3)
        	h.cmdPrint("tc qdisc add dev s1-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's2':
	    for n in range(10):
		randDelay = random.randint(1,3)
        	h.cmdPrint("tc qdisc add dev s2-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's3':
	    for n in range(10):
		randDelay = random.randint(1,5)
        	h.cmdPrint("tc qdisc add dev s3-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's4':
	    for n in range(10):
		randDelay = random.randint(1,3)
        	h.cmdPrint("tc qdisc add dev s4-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's5':
	    for n in range(10):
		randDelay = random.randint(1,4)
        	h.cmdPrint("tc qdisc add dev s5-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's6':
	    for n in range(10):
		randDelay = random.randint(1,5)
        	h.cmdPrint("tc qdisc add dev s6-eth%d root netem delay %dms"%(n+1, randDelay))


        elif h.name == 's7':
	    for n in range(10):
		randDelay = random.randint(1,5)
        	h.cmdPrint("tc qdisc add dev s7-eth%d root netem delay %dms"%(n+1, randDelay))


        #elif h.name == 's8':
	#    for n in range(10):
	#	randDelay = random.randint(1,4)
        #	h.cmdPrint("tc qdisc add dev s8-eth%d root netem delay %dms"%(n+1, randDelay))
	
        #elif h.name == 's9':
	#    for n in range(10):
	#	randDelay = random.randint(1,3)
        #	h.cmdPrint("tc qdisc add dev s9-eth%d root netem delay %dms"%(n+1, randDelay))


        #elif h.name == 's10':
	#    for n in range(10):
	#	randDelay = random.randint(1,5)
        #	h.cmdPrint("tc qdisc add dev s10-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's11':
	    h.cmdPrint("tc qdisc add dev s1-eth11 root netem delay 5ms")

        elif h.name == 's12':
            h.cmdPrint("tc qdisc add dev s2-eth11 root netem delay 5ms")

        elif h.name == 's13':
            h.cmdPrint("tc qdisc add dev s3-eth11 root netem delay 5ms")

        elif h.name == 's14':
            h.cmdPrint("tc qdisc add dev s4-eth11 root netem delay 5ms")
	    
        elif h.name == 's15':
            h.cmdPrint("tc qdisc add dev s5-eth11 root netem delay 5ms")

        elif h.name == 's16':
            h.cmdPrint("tc qdisc add dev s6-eth11 root netem delay 5ms")

        elif h.name == 's17':
            h.cmdPrint("tc qdisc add dev s7-eth11 root netem delay 5ms")

        #elif h.name == 's18':
        #    h.cmdPrint("tc qdisc add dev s8-eth11 root netem delay 5ms")

        #elif h.name == 's19':
        #    h.cmdPrint("tc qdisc add dev s9-eth11 root netem delay 5ms")

        #elif h.name == 's20':
        #    h.cmdPrint("tc qdisc add dev s10-eth11 root netem delay 5ms")
    CLI(net)
    #for h in net.hosts:
#	if h.name.startswith('g'):
#	    randDelay = random.randint(0,4)
#	    #h.cmdPrint("tc qdisc add dev %s-eth0 root netem delay 0ms %dms"%(h.name, randDelay))
#	    h.cmdPrint('python -m SimpleHTTPServer 8080 &')

    #for h in net.hosts:
#	if h.name.startswith('h') and h.name in ['h1', 'h2', 'h3','h4', 'h5', 'h6', 'h7','h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20']:
#	    h.cmdPrint('python main.py %s &'%h.IP())
	
#    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()
