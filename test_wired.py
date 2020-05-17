from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, UserSwitch  
import random
import time

class MultiSwitchTopo(Topo):
    "multiple switch connected to n hostst"
    def build(self):
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4','10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9','10.0.0.10']
        addresses2 = ['10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14','10.0.0.15','10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20']
        addresses3 = ['10.0.0.21', '10.0.0.22', '10.0.0.23', '10.0.0.24','10.0.0.25','10.0.0.26', '10.0.0.27', '10.0.0.28', '10.0.0.29', '10.0.0.30']
        addresses4 = ['10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34','10.0.0.35','10.0.0.36', '10.0.0.37', '10.0.0.38', '10.0.0.39', '10.0.0.40']

        
        gwAddresses = ['10.0.0.41', '10.0.0.42', '10.0.0.43', '10.0.0.44','10.0.0.45','10.0.0.46', '10.0.0.47', '10.0.0.48', '10.0.0.49', '10.0.0.50']
        
        switch = self.addSwitch('s13', cls=OVSKernelSwitch)

        switch1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s3', cls=OVSKernelSwitch)
        switch4 = self.addSwitch('s4', cls=OVSKernelSwitch)
        switch5 = self.addSwitch('s5', cls=OVSKernelSwitch)
        switch6 = self.addSwitch('s6', cls=OVSKernelSwitch)

        switch7 = self.addSwitch('s7', cls=OVSKernelSwitch)
        switch8 = self.addSwitch('s8', cls=OVSKernelSwitch)
        switch9 = self.addSwitch('s9', cls=OVSKernelSwitch)
        switch10 = self.addSwitch('s10', cls=OVSKernelSwitch)
        switch11 = self.addSwitch('s11', cls=OVSKernelSwitch)
        switch12 = self.addSwitch('s12', cls=OVSKernelSwitch)
        
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

        self.addLink(switch7, switch1)
        self.addLink(switch8, switch2)
        self.addLink(switch9, switch3)
        self.addLink(switch10, switch4)
        self.addLink(switch11, switch5)
        self.addLink(switch12, switch6)

        self.addLink(switch, switch7)
        self.addLink(switch, switch8)
        self.addLink(switch, switch9)
        self.addLink(switch, switch10)
        self.addLink(switch, switch11)
        self.addLink(switch, switch12)


        for g in range(len(gwAddresses)):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch)
            
            

def simpleTest():
    topo = MultiSwitchTopo()
    net = Mininet(topo)
    net.start()
    print("Dumping host connection")
    popens = {}
    for h in net.hosts:
        if h.name.startswith('g'):
            randDelay = random.randint(1,4)
            h.cmdPrint("tc qdisc add dev %s-eth0 root netem delay 0ms %dms"%(h.name, randDelay))
   
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
      
        elif h.name == 's7':
            randDelay = random.randint(1,3)
            h.cmdPrint("tc qdisc add dev s1-eth11 root netem delay %dms"%(randDelay))

        elif h.name == 's8':
            h.cmdPrint("tc qdisc add dev s2-eth11 root netem delay 5ms")

        elif h.name == 's9':
            h.cmdPrint("tc qdisc add dev s3-eth11 root netem delay 5ms")

        elif h.name == 's10':
            h.cmdPrint("tc qdisc add dev s4-eth11 root netem delay 5ms")

    
    for h in net.hosts:
        if h.name.startswith('g'):
            h.cmdPrint('nohup python -m SimpleHTTPServer 8080 &')
            time.sleep(3)

    for h in net.hosts:
        if h.name.startswith('h'):
            h.cmdPrint('nohup python main.py %s &'%h.IP())
            time.sleep(10)
                        
    CLI(net)
if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()