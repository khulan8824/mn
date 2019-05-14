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
    topK=10
    senseCount = 0
    sendCount = 0
    receiveCount = 0

    ####################TRUST SCORE CALCULATION################
    #########################Non transitive###################
    ####Mean of the same gateway latency that others sent vs my value
    def calculateTrustScore(self, node, l):
        
        gateways = {x for x in self.logs if x.sender==node and (datetime.datetime.now() - x.ts).seconds < self.period} 
        value = 0.0
        samples = []
        for g in l:
            rest = {v for v in self.logs if v.sender!= node and (datetime.datetime.now() - v.ts).seconds < (self.period*2) and v.address == g.address}
            total = 0.0
            for r in rest:
                total += float(r.latency)
                samples.append(r.latency)
            mean =0.0
            if len(rest)>0:
                mean = total / len(rest)
            value += abs(mean - float(g.latency))
        if len(l)>0:
            value = value / len(l)
        
        if node in self.trustScore.keys():
            self.trustScore[node] = 0.33*self.trustScore[node] + 0.66*value
        else:
            self.trustScore[node] = 1.0*value
        
    def checkNodeActive(self):        
        for n in self.closeNeighbors:
            values = [v for v in self.logs if v.sender == n and (datetime.datetime.now() - v.ts).seconds < (self.period*3+10)]
            if len(values)==0:
                if n in self.trustScore:
                    print('Not received from', n)
                    self.trustScore.update({n:2})                
                
        
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
        if int(code) != 200:
            return ""
        else:
            with open('log','a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(address.encode('ascii', 'ignore')),str(lat.encode('ascii', 'ignore')), str(self.myAddress), str(self.myAddress)))
            return float(lat)
        
    def setGatewayTable(self, ts, address,latency,sender):
        if sender not in self.closeNeighbors:
            self.checkNeighbor(sender)
        delete = [key for key in self.gatewayTable if (datetime.datetime.now() - self.gatewayTable[key].ts).seconds > (self.period+10)]
        #print('deleting:', delete)
        for key in delete: del self.gatewayTable[key] 
        gateway = gw.Gateway(ts, address, latency, sender)
        if sender != self.myAddress:
            gateway.actualLatency  = self.pingGateway(address)
        if sender in dict(sorted(self.trustScore.items(),key=lambda kv: kv[1])[:self.topK]) or len(self.trustScore)<=self.topK or sender == self.myAddress:
            previous_gws= self.get2RecentGateways(gateway)
            cnt = 1
            value = 0
            for gway in previous_gws:
                value += (gway.latency*cnt)/(sum(range(len(previous_gws)+2)))
                cnt+=1
            if len(previous_gws) == 0:
                self.gatewayTable[address] = gateway
            else:
                gateway.latency =value + (cnt*gateway.latency)/(sum(range(1,len(previous_gws)+2)))
                self.gatewayTable[address] = gateway
        self.logs.append(gateway)

    def printGatewayTable(self):
        for gw in self.gatewayTable:
            with open('gw_table_'+self.myAddress,'a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(self.gatewayTable[gw].address), str(self.gatewayTable[gw].latency), str(self.gatewayTable[gw].actualLatency), str(self.gatewayTable[gw].sender)))
            
    def sense(self):
        gws = self.select2Random()
        txt = ""
        for g in gws:
            lat = self.pingGateway(g)
            self.senseCount += 1
            print(g, lat)
            self.setGatewayTable(datetime.datetime.now(), g, float(lat), self.myAddress)
            
            ######ADDING FAULTY FEATURES#######
            #if self.myAddress in ['10.0.0.3', '10.0.0.13', '10.0.0.23', '10.0.0.33', '10.0.0.43', '10.0.0.53', '10.0.0.63',
            #                     '10.0.0.73', '10.0.0.83'
            #                      ,'10.0.0.5', '10.0.0.15', '10.0.0.25', '10.0.0.35', '10.0.0.45', 
            #                      '10.0.0.55', '10.0.0.65','10.0.0.75', '10.0.0.85'
                                  #,'10.0.0.7', '10.0.0.17', '10.0.0.27','10.0.0.37', '10.0.0.47','10.0.0.57', 
                                  #'10.0.0.67','10.0.0.77', '10.0.0.87'
            #                     ]:#,'10.0.0.9', 
                                  #'10.0.0.19', '10.0.0.29','10.0.0.39', '10.0.0.49','10.0.0.59', '10.0.0.69','10.0.0.79',
                                  #'10.0.0.89']:
             #   print('prev lat:',lat)
             #   lat = float(lat)*10
             #   print('edited lat:',lat)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+','+str(g)+","+str(lat)+","+self.myAddress
            if txt =="":
                txt += t
            else:
                txt = txt+"#"+t
                
        trust_score =sorted(self.trustScore.items(),key=lambda kv: kv[1])
        trust_score =dict(sorted(self.trustScore.items(),key=lambda kv: kv[1])[:self.topK])
        addr = trust_score.keys()
        
        self.checkNodeActive()
        
        if len(trust_score)<2:
            addr = self.closeNeighbors
        for n in addr:
            if n in self.closeNeighbors:
                self.sendCount += 1
            if n == self.myAddress:
                continue
            f = protocol.ClientFactory()
            f.protocol = client.MessageClientProtocol        
            f.protocol.addr = n
            f.protocol.text = txt
            reactor.connectTCP(n, 5555, f)
            if not reactor.running:
                reactor.run()
                
        #self.printGatewayTable()
        #self.printCosineSimilarity()
        
    def send(self):
        self.cnt+=1	
        self.topK = len(self.gateways)/2+1
        #self.gatewayTable = {}
        if self.cnt <400:            
            reactor.callLater(self.period, self.send)
            self.sense()
            self.printGatewayTable()
            #self.printCount()
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
        l = [x for x in self.gatewayTable if (datetime.datetime.now() - self.gatewayTable[x].ts).seconds <= (self.period+10)]
        return l
    
    def get2RecentGateways(self, gateway):
        l = [x for x in self.logs if (datetime.datetime.now() - x.ts).seconds <= (self.period*2) and x.address == gateway.address]

        return l

    
    def printCount(self):
        with open('count_'+self.myAddress,'a') as f:
                f.write("{0},{1},{2},{3}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(self.senseCount), str(self.sendCount), str(self.receiveCount)))                
                self.senseCount = 0
                self.sendCount = 0
                self.receiveCount = 0
                
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
        
        trust_score =sorted(self.trustScore.items(),key=lambda kv: kv[1])[:self.topK]
        with open('sim_'+self.myAddress,'a') as f:
            f.write("{0},{1},{2},{3}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(sim), str(len(recent)), len(self.closeNeighbors)))
        print('Total recent measurement sim:',':',sim,len(recent),len(trust_score))

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
        
    def checkNeighbor(self, node):        
        print('Checking neighbor', node)
        if node == self.myAddress:
            return
        rtt = self.ping(node)
        if rtt < self.trshld:
            self.closeNeighbors.append(node)
            print('appending',node)
            
    def senseNeighbors(self):
        for n in self.neighbors:
            if n == self.myAddress:
                continue
            rtt = self.ping(n)
            #print(n, rtt)
            if rtt<self.trshld:
                self.closeNeighbors.append(n)
        print("Close neighbors", self.closeNeighbors)
