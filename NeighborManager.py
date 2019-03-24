import random
import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os
import sys
from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

import MessageServerProtocol as server
import MessageClientProtocol as client
import Gateway as gw

class NeighborManager:
    neighborAddress= ""
    neighbors = []
    closeNeighbors = []
    gateways = []
    gatewayTable = {}
    actualTable={}
    myAddress = ""
    trshld = 1
    cnt = 0
    
    
    ########HELPER FUNCTIONS#######
    def select2Random(self):
        status = True
        if len(self.gateways)>2:               
            return random.sample(set(self.gateways), 2)
        else:
            return self.gateways
        
    def pingGateway(self,address):
        status = True
        cmd='''curl http://'''+address+''':8080/1Mb.dat -m 180 -w %{time_total},%{http_code} -o /dev/null -s'''
        print(cmd)
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        print(stdout.decode("utf-8").split(','))
        lat, code = stdout.decode("utf-8").split(',')
        #print(lat, code)
        if int(code) != 200:
            return ""
        else:
            self.setGatewayTable(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                 address, float(lat), self.myAddress)
            with open('log','a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(address),str(lat), str(self.myAddress), str(self.myAddress)))
            return float(lat)
        
    def setGatewayTable(self, ts,address,latency,sender):
        gateway = gw.Gateway(ts, address, latency, sender)
        
        if address != self.myAddress:
            gateway.actualLatency  = self.pingGateway(address)
            
        self.gatewayTable[address] = gateway
            
    def sense(self):
        gws = self.select2Random()
        txt = ""
        for gw in gws:
            lat = self.pingGateway(gw)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+','+str(gw)+","+str(lat)+","+self.myAddress
            if txt =="":
                txt += t
            else:
                txt = txt+"#"+t
        #print("txt :",txt)
        for n in self.closeNeighbors:
            if n == self.myAddress:
                continue
            f = protocol.ClientFactory()
            f.protocol = client.MessageClientProtocol        
            f.protocol.addr = n
            f.protocol.text = txt
            reactor.connectTCP(n, 5555, f)
            if not reactor.running:
                reactor.run()
        
    def send(self):
        self.cnt+=1
        if self.cnt <20:            
            reactor.callLater(60, self.send)
            self.sense()
            for gw in self.gatewayTable:
                gw.printInformation()
        else:
            print("END")
            #sys.exit(0)
    
    def ping(self, address):
        cmd='ping -w 5 -c 3 -q '+address
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        stdout = str(stdout)
        if '/' not in stdout:
            return 0
        else:
            return float(stdout.split('/')[-3])
        
    
    def senseNeighbors(self):
        for n in self.neighbors:
            if n == self.myAddress:
                continue
            rtt = self.ping(n)
            print(n, rtt)
            if rtt<self.trshld:
                self.closeNeighbors.append(n)
        print("Close neighbors", self.closeNeighbors)