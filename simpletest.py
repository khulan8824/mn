from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

class SingleSwitchTopo(Topo):
	#"Single switch connected to n hostst"
	def build(self, n=2):
		switch = self.addSwitch('s1')
		for h in range(n):
			host = self.addHost('h%s' % (h+1))
			self.addLink(host, switch)
		for gw in range(2):
			gw = self.addHost('g%s' % (gw+1))
			self.addLink(gw, switch)
def simpleTest():
	topo = SingleSwitchTopo(n=4)
	net = Mininet(topo)
	net.start()
	print("Dumping host connection")
	#net.pingAll()
	#net.stop()
	CLI(net)

if __name__ == "__main__":
	setLogLevel('info')
	simpleTest()
