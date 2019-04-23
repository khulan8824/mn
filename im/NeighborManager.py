import random
import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os
import sys
from math import *



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
    logs = [] # Add
    trustScore = {}
    myAddress = ""
    trshld = 1
    cnt = 0
    period = 60

    
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
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')
        code = int(code)
        #print(lat, code)
        if int(code) != 200:
            return ""

        return float(lat)
        
    def setGatewayTable(self, ts, address,latency,sender):
        #setGatewayTable(datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"), str(address) ,latency,str(sender))
        gateway = gw.Gateway(ts, address, latency, sender)
        if sender != self.myAddress:
            gateway.actualLatency  = self.pingGateway(address)
        self.gatewayTable[address] = gateway

    def printGatewayTable(self):
        print("==========GW TABLE=====")
        for gw in self.gatewayTable:
            print(self.gatewayTable[gw].address,self.gatewayTable[gw].latency,
                      self.gatewayTable[gw].actualLatency,self.gatewayTable[gw].sender)
            with open('gw_table_'+self.myAddress,'a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(self.gatewayTable[gw].address), str(self.gatewayTable[gw].latency), str(self.gatewayTable[gw].actualLatency), str(self.gatewayTable[gw].sender)))
            
    def sense(self):
        gws = self.select2Random()
        txt = ""
        print('sensing')
        for gw in gws:
                
            lat = self.pingGateway(gw)
            print(gw, ':', lat)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+','+str(gw)+","+str(lat)+","+self.myAddress
            self.setGatewayTable(datetime.datetime.now(), gw, float(lat), self.myAddress)
            if txt =="":
                txt += t
            else:
                txt = txt+"#"+t

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
        self.printGatewayTable()
        self.printCosineSimilarity()
        
    def send(self):
        self.cnt+=1
        if self.cnt <400:            
            reactor.callLater(self.period, self.send)
            self.sense()
        else:
            print("END")

####################COSINE SIMILARITY#################
    def square_rooted(self, x): 
        return round(sqrt(sum([a*a for a in x])),3)

    def cosine_similarity(self, x,y):
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        return round(numerator/float(denominator),3)

    def getRecentGateways(self):
        return [x for x in self.gatewayTable if (datetime.datetime.now() - self.gatewayTable[x].ts).seconds <= (self.period*2)]


    def printCosineSimilarity(self):
        total = 0
        count1 = 0
        recent = self.getRecentGateways()
        print("=======================COSINE SIMILARITY MEASUREMENT================")
        #print([x.address for x in recent])
        m1 = []
        m2 = []
        for gw in recent:
            m1.append(float(self.gatewayTable[gw].latency))
            m2.append(float(self.gatewayTable[gw].actualLatency))

        sim = float(self.cosine_similarity(m1,m2))
        with open('sim_'+self.myAddress,'a') as f:
            f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(sim)))
        print('Total recent measurement sim:',':',sim)

#######################SENSING#######################    
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
