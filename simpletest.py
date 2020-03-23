from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, UserSwitch 
from mininet.node import CPULimitedHost
import random

class CustomTreeTopo(Topo):
    "Single switch connected to n hostst"
    def build(self, n=2):
                
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5',
                     '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9', '10.0.0.10',
                      '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14', '10.0.0.15']

        addresses2 = ['10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19', '10.0.0.20',
                      '10.0.0.21','10.0.0.22']
        

        addresses3 =  ['10.0.0.23', '10.0.0.24', '10.0.0.25', '10.0.0.26','10.0.0.27',
                       '10.0.0.28', '10.0.0.29', '10.0.0.30', '10.0.0.31', '10.0.0.32',
                       '10.0.0.33', '10.0.0.34']
        
        addresses4 = ['10.0.0.35', '10.0.0.36', '10.0.0.37', '10.0.0.38', '10.0.0.39',
                     '10.0.0.40']
        
                      
        addresses5 = ['10.0.0.41','10.0.0.42', '10.0.0.43', '10.0.0.44', '10.0.0.45', 
                      '10.0.0.46', '10.0.0.47', 
                      '10.0.0.48']
        
        
        gwAddresses = ['10.0.0.91', '10.0.0.92', '10.0.0.93', '10.0.0.94', '10.0.0.95',
                      '10.0.0.96', '10.0.0.97', '10.0.0.98', '10.0.0.99', '10.0.0.100']

        
        switch = self.addSwitch('s6', cls=OVSKernelSwitch)
        switch1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s3', cls=OVSKernelSwitch)        
        switch4 = self.addSwitch('s4', cls=OVSKernelSwitch)        
        switch5 = self.addSwitch('s5', cls=OVSKernelSwitch)  

        for h in range(15):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)
        
        for h in range(7):
            host = self.addHost('h%s'% (h+len(addresses1)+1), ip=addresses2[h])
            self.addLink(host, switch2)
        
        for h in range(12):
            host = self.addHost('h%s'% (h+len(addresses1)+len(addresses2)+1), ip=addresses3[h])
            self.addLink(host, switch3)
            
        for h in range(6):
            host = self.addHost('h%s'% (h+len(addresses1)+len(addresses2)+len(addresses3)+1), ip=addresses4[h])
            self.addLink(host, switch4)
        
            
        for h in range(8):
            host = self.addHost('h%s'% (h+len(addresses1)+len(addresses2)+len(addresses3)+len(addresses4)+1), ip=addresses5[h])
            self.addLink(host, switch5)
            
            
        
        self.addLink(switch, switch1)
        self.addLink(switch, switch2)
        self.addLink(switch, switch3)
        self.addLink(switch, switch4)
        self.addLink(switch, switch5)        
        #self.addLink(switch, switch6)           
        #self.addLink(switch, switch7)
        
        for g in range(10):            
            randDelay = random.uniform(0.8,1)
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g], cpu = randDelay)
            self.addLink(gw, switch)
            
            

def simpleTest():
    
    topo = CustomTreeTopo(n=4)
    net = Mininet(topo, host=CPULimitedHost)
    
    #c1 = net.addController('c1', controller=RemoteController,ip="127.0.0.1", port=6633)
    net.start()
    #c1.start()
    #for s in net.switches:
    #    s.start([c1])
        
    
    print("Dumping host connection")
    popens = {}
    
    for h in net.switches:
        if h.name == 's1':
            for n in range(15):
                randDelay = random.randint(1,3)
                h.cmdPrint("tc qdisc add dev s1-eth%d root netem delay %dms"%(n+1, randDelay))
        
        elif h.name == 's2':
            for n in range(7):
                randDelay = random.randint(0,4)
                h.cmdPrint("tc qdisc add dev s2-eth%d root netem delay %dms"%(n+1, randDelay))
                
        elif h.name == 's3':
            for n in range(12):
                randDelay = random.randint(1,4)
                h.cmdPrint("tc qdisc add dev s3-eth%d root netem delay %dms"%(n+1, randDelay))
                
        if h.name == 's4':
            for n in range(6):
                randDelay = random.randint(0,5)
                h.cmdPrint("tc qdisc add dev s4-eth%d root netem delay %dms"%(n+1, randDelay))
                
        if h.name == 's5':
            for n in range(8):
                randDelay = random.randint(1,4)
                h.cmdPrint("tc qdisc add dev s5-eth%d root netem delay %dms"%(n+1, randDelay))
                
        elif h.name == 's6':
            h.cmdPrint("tc qdisc add dev s1-eth16 root netem delay 5ms")
            h.cmdPrint("tc qdisc add dev s2-eth8 root netem delay 4ms")
            h.cmdPrint("tc qdisc add dev s3-eth13 root netem delay 4ms")
            h.cmdPrint("tc qdisc add dev s4-eth7 root netem delay 5ms")
            h.cmdPrint("tc qdisc add dev s5-eth9 root netem delay 5ms")            
            

    CLI(net)
    
    #for h in net.hosts:
    #    if h.name.startswith('h'):
    #        h.cmdPrint('python main.py %s &'%(h.IP()))
    
    #CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    simpleTest()