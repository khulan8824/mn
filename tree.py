from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.topolib import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import CPULimitedHost
import random

class GenericTree(Topo):
    """Simple topology example."""
    def build( self, depth=1, fanout=2 ):
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1

    def build( self, depth=1, fanout=2 ):
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
        # Build topology
        self.addTree(depth, fanout)

    def addTree( self, depth, fanout ):
        """Add a subtree starting with node n.
           returns: last node added"""
        isSwitch = depth > 0
        if isSwitch:
            node = self.addSwitch( 's%s' % self.switchNum )
            self.switchNum += 1
            for _ in range( fanout ):
                child = self.addTree( depth - 1, fanout )
                self.addLink( node, child )
        else:
            if self.hostNum>90:
                cpuLimit = [.8, .3, .9]
                l =  random.choice(cpuLimit)
                print(self.hostNum, l)
                node = self.addHost( 'h%s' % self.hostNum, cpu =l)
            else:
                node = self.addHost( 'h%s' % self.hostNum )
            self.hostNum += 1
        return node

setLogLevel('info')
tree4 = GenericTree(depth=2,fanout=10)
net = Mininet(topo=tree4, host=CPULimitedHost)
net.start()

for h in net.switches:
    if h.name=='s2':
        for n in range(10):
            randDelay = random.randint(1,3)
            h.cmdPrint("tc qdisc add dev s2-eth%d root netem delay %dms"%(n+1, randDelay))

    elif h.name == 's11':
        for n in range(10): 
            randDelay = random.randint(5,10)
            h.cmdPrint("tc qdisc add dev s11-eth%d root netem delay %dms"%(n+1, randDelay))
            name = 'h9%d'%(n+1)
            if n == 9:
                name = 'h100'
            node = net.getNodeByName(name)
            link = h.connectionsTo(node)

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


    elif h.name == 's8':
        for n in range(10):
            randDelay = random.randint(1,4)
            h.cmdPrint("tc qdisc add dev s8-eth%d root netem delay %dms"%(n+1, randDelay))

    elif h.name == 's9':
        for n in range(10):
            randDelay = random.randint(1,3)
            h.cmdPrint("tc qdisc add dev s9-eth%d root netem delay %dms"%(n+1, randDelay))


    elif h.name == 's10':
        for n in range(10):
            randDelay = random.randint(2,6)
            h.cmdPrint("tc qdisc add dev s10-eth%d root netem delay %dms"%(n+1, randDelay))

    elif h.name == 's1':
        h.cmdPrint("tc qdisc add dev s2-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s3-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s4-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s5-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s6-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s7-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s8-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s9-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s10-eth11 root netem delay 5ms")
        h.cmdPrint("tc qdisc add dev s11-eth11 root netem delay 5ms")

CLI(net)

#for h in net.hosts:
#    if h.name not in ['h91', 'h92', 'h93','h94', 'h95', 'h96', 'h97','h98', 'h99', 'h100']:
#        h.cmdPrint('python main.py %s &'%h.IP())
#CLI(net)