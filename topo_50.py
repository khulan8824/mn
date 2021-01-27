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
        
        addresses5 = ['10.0.0.41', '10.0.0.42', '10.0.0.43', '10.0.0.44','10.0.0.45','10.0.0.46', '10.0.0.47', '10.0.0.48', '10.0.0.49', '10.0.0.50']
       
        gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5', '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']
        
        switch = self.addSwitch('s13', cls=OVSKernelSwitch)

        switch1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s3', cls=OVSKernelSwitch)
        switch4 = self.addSwitch('s4', cls=OVSKernelSwitch)
        switch5 = self.addSwitch('s5', cls=OVSKernelSwitch)

       
        switch7 = self.addSwitch('s7', cls=OVSKernelSwitch)
        switch8 = self.addSwitch('s8', cls=OVSKernelSwitch)
        switch9 = self.addSwitch('s9', cls=OVSKernelSwitch)
        switch10 = self.addSwitch('s10', cls=OVSKernelSwitch)
        switch11 = self.addSwitch('s11', cls=OVSKernelSwitch)
        
        for h in range(len(addresses1)):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)

        for h in range(len(addresses2)):
            host = self.addHost('h%s' % (len(addresses1)+h+1), ip=addresses2[h])
            self.addLink(host, switch2)

        for h in range(len(addresses3)):
            host = self.addHost('h%s' % (len(addresses1)*2+h+1), ip=addresses3[h])
            self.addLink(host, switch3)
            
        for h in range(len(addresses4)):
            host = self.addHost('h%s' % (len(addresses1)*3+h+1), ip=addresses4[h])
            self.addLink(host, switch4)
            
        for h in range(len(addresses5)):
            host = self.addHost('h%s' % (len(addresses1)*4+h+1), ip=addresses5[h])
            self.addLink(host, switch5)
            
        self.addLink(switch7, switch1)
        self.addLink(switch8, switch2)
        self.addLink(switch9, switch3)
        self.addLink(switch10, switch4)
        self.addLink(switch11, switch5)
        
        self.addLink(switch, switch7)
        self.addLink(switch, switch8)        
        self.addLink(switch, switch9)
        self.addLink(switch, switch10)
        self.addLink(switch, switch11)


        for g in range(len(gwAddresses)):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch)            
            

def topo():
    topo = MultiSwitchTopo()
    net = Mininet(topo)
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
                randDelay = random.randint(3,6)
                h.cmdPrint("tc qdisc add dev s4-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's5':
            for n in range(10):
                randDelay = random.randint(2,6)
                h.cmdPrint("tc qdisc add dev s5-eth%d root netem delay %dms"%(n+1, randDelay))
                
        elif h.name == 's7':
            h.cmdPrint("tc qdisc add dev s7-eth1 root netem delay 5ms")   
        elif h.name == 's8':
            h.cmdPrint("tc qdisc add dev s8-eth1 root netem delay 5ms")   
        elif h.name == 's9':
            h.cmdPrint("tc qdisc add dev s9-eth1 root netem delay 5ms")   
        elif h.name == 's10':
            h.cmdPrint("tc qdisc add dev s10-eth1 root netem delay 5ms")   
        elif h.name == 's11':
            h.cmdPrint("tc qdisc add dev s11-eth1 root netem delay 5ms")
            

        #elif h.name == 's8':
        #    h.cmdPrint("tc qdisc add dev s2-eth11 root netem delay 5ms")

        #elif h.name == 's9':
        #    h.cmdPrint("tc qdisc add dev s3-eth11 root netem delay 5ms")

        #elif h.name == 's10':
        #    h.cmdPrint("tc qdisc add dev s4-eth11 root netem delay 5ms")    
        #elif h.name == 's11':
        #    h.cmdPrint("tc qdisc add dev s5-eth11 root netem delay 5ms")

        #elif h.name == 's12':
        #    h.cmdPrint("tc qdisc add dev s6-eth11 root netem delay 5ms")
        
    for h in net.hosts:
        if h.name =='g1':
            h.cmdPrint("tc qdisc add dev g1-eth0 root netem delay 2ms")
        elif h.name =='g2':
            h.cmdPrint("tc qdisc add dev g2-eth0 root netem delay 3ms")
        elif h.name =='g3':
            h.cmdPrint("tc qdisc add dev g3-eth0 root netem delay 4ms")
        elif h.name =='g4':
            h.cmdPrint("tc qdisc add dev g4-eth0 root netem delay 2ms")            
        elif h.name =='g5':
            h.cmdPrint("tc qdisc add dev g5-eth0 root netem delay 1ms")            
        elif h.name =='g7':
            h.cmdPrint("tc qdisc add dev g7-eth0 root netem delay 4ms")
        elif h.name =='g8':
            h.cmdPrint("tc qdisc add dev g8-eth0 root netem delay 1ms")
        elif h.name =='g10':
            h.cmdPrint("tc qdisc add dev g10-eth0 root netem delay 3ms")
            


    #for h in net.hosts:
    #    if h.name.startswith('g'):
    #        h.cmdPrint('nohup python -m SimpleHTTPServer 8080 &')
            
    #for h in net.hosts:
    #    if h.name.startswith('h') and h.name in ['h1', 'h2', 'h3','h4', 'h5', 'h6', 'h7','h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21','h22', 'h23', 'h24','h24','h25','h26','h27','h28', 'h29',
    #                                            'h30','h31','h32','h33','h34','h35','h36','h37','h38','h39','h40','h41','h42'
    #                                            ,'h43','h44','h45','h46','h47','h48','h49','h50']:
    #        h.cmdPrint('nohup python main.py %s &'%h.IP())            
    #        time.sleep(2)

    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    topo()