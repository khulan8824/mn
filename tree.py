from mininet.net import Mininet
from mininet.topolib import TreeTopo

from mininet.cli import CLI
import random

tree4 = TreeTopo(depth=2,fanout=10)
net = Mininet(topo=tree4)
net.start()

for h in net.switches:
    if h.name=='s2':
        for n in range(10):
            randDelay = random.randint(1,3)
            h.cmdPrint("tc qdisc add dev s2-eth%d root netem delay %dms"%(n+1, randDelay))

    elif h.name == 's11':
        for n in range(10): 
            randDelay = random.randint(1,3)
            h.cmdPrint("tc qdisc add dev s11-eth%d root netem delay %dms"%(n+1, randDelay))

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
            randDelay = random.randint(5,10)
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