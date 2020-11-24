import random
import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os
import sys
from math import *
import statistics 
from statistics import stdev 
import numpy as np
from sklearn.linear_model import LinearRegression


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
    originalGateways = []
    gatewayTable = {}
    logs = [] # Historical gw perf table values
    trustScore = {} #updated trust score of each collaborators
    myAddress = ""
    trshld = 1
    cnt = 0
    period = 60
    topK=10
    senseCount = 0
    sendCount = 0
    receiveCount = 0
    gateway_candidates = []
    selection_candidates = []
    selected_gateway = ""
    selected_best_gateway = ""
    selected_random_gateway = ""
    selected_all_best_gateway = ""
    trshldLat = 0
    trshldDev = 0

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
            values = [v for v in self.logs if v.sender == n and (datetime.datetime.now() - v.ts).seconds < (self.period+30)]
            if len(values)==0:
                if n in self.trustScore:
                    old_score = self.trustScore.get(n)                    
                    score = old_score*0.33                    
                    #print('Not received from', n, old_score, score)
                    self.trustScore.update({n:score})
                
        
    ########HELPER FUNCTIONS#######
    #return 2 random gateway nodes from the list of gateways
    def select2Random(self):
        self.gateway_candidates = []
        devs = []
        if self.cnt%2 == 1 and len(self.logs)>0:                
            for g in self.gateways:
                gw_info = []
                if len(self.logs)>0:
                    for g1 in self.logs:
                        if g1.address == g:
                                gw_info.append(g1.latency)
                
                if gw_info != None and len(gw_info)>=2:
                    devs.append(statistics.stdev(gw_info))
                    #print(g,statistics.stdev(gw_info))
                    if statistics.stdev(gw_info)< self.trshldDev:
                        self.gateway_candidates.append(g)
        else:
            self.gateway_candidates = self.gateways
        #print(self.gateway_candidates)
        status = True
        if len(self.gateway_candidates)>2:               
            return random.sample(set(self.gateway_candidates), 2)
        else:
            return self.gateway_candidates
        
#Downloading 1mb file from the local HTTP server used as a gateway node
#returning the download latency to the caller
    def pingGateway(self,address):
        status = True
        #cmd='''curl http://'''+address+''':8080/1Mb.dat -m 300 -w %{time_total},%{http_code} -o /dev/null -s'''
        cmd='''curl -x '''+address+''':3128 -U david.pinilla:"|Jn 5DJ\\7inbNniK|m@^ja&>C" -m 180 -w %{time_total},%{http_code} http://ovh.net/files/1Mb.dat -o /dev/null -s'''
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')
        
        #Checking if gateway is accessible
        if int(code) != 200:
            #print(address," not accessible")
            #self.gateways.remove(address)
            return ""
        else:
            with open('log','a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(address.encode('ascii', 'ignore')),str(lat.encode('ascii', 'ignore')), str(self.myAddress), str(self.myAddress)))
            return float(lat)

# update gateway table with new sender and latency of the gateways. 
    def setGatewayTable(self, ts, address,latency,sender):
        if latency == "" or latency is None:
            return
        if sender not in self.closeNeighbors:
            self.checkNeighbor(sender)
        delete = [key for key in self.gatewayTable if (datetime.datetime.now() - self.gatewayTable[key].ts).seconds > (self.period+10)]
        for key in delete: 
            del self.gatewayTable[key] 
        gateway = gw.Gateway(ts, address, latency, sender)

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
        gateway.stdev = self.getRecentDeviation(10, gateway) #Finding out the std of the specific gateway
        self.updateThresholdValues()
        gateway = self.setCategory(gateway)
        
        #checking if the received gw is in the gateway list?
        if address not in self.gateway_candidates:
            self.gateway_candidates.append(address)
        self.logs.append(gateway)
        
    def setCategory(self, gateway):
        if gateway.latency < self.trshldLat and gateway.stdev < self.trshldDev:
            gateway.category = "good"
        elif gateway.latency < self.trshldLat and gateway.stdev > self.trshldDev:
            gateway.category = "inconsistent"
        elif gateway.latency > self.trshldLat and gateway.stdev < self.trshldDev:
            gateway.category = "inconsistent"
        elif gateway.latency > self.trshldLat and gateway.stdev > self.trshldDev:
            gateway.category = "bad"
        return gateway 
    
    def printGatewayTable(self, gatewayTable):
        #for gw in self.gatewayTable:
        for gw in gatewayTable:
            print(gw.ts.strftime("%Y-%m-%d %H:%M:%S"), str(gw.address), str(gw.latency), str(gw.stdev),gw.category)

#Sensing gateway nodes performances and sending to the close neighboers
    def sense(self):
        if len(self.closeNeighbors)<1:
            self.senseNeighbors()
        self.senseGateways()
        gws = self.select2Random()
        txt = ""
        for g in gws:
            lat = self.pingGateway(g)
            self.senseCount += 1
            #print("latency to",g,lat)
            if str(lat) == "":
                continue
            self.setGatewayTable(datetime.datetime.now(), g, float(lat), self.myAddress)          
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+','+str(g)+","+str(lat)+","+self.myAddress
            if txt =="":
                txt += t
            else:
                txt = txt+"#"+t
                
        #filter topK trusted neighbors into addr        
        trust_score =sorted(self.trustScore.items(),key=lambda kv: kv[1])
        trust_score =dict(sorted(self.trustScore.items(),key=lambda kv: kv[1])[:self.topK])
        addr = trust_score.keys()
        
        self.checkNodeActive()
        
        if len(trust_score)<2:
            addr = self.closeNeighbors
        #Connecting with close neighbors through their IP address and 5555 port
        #txt variable contains all the measurements to be sent
        
        #print("Sending<<<",len(addr),addr)
        print("============Trust scores=============")
        for n in self.trustScore:
            print(n, self.trustScore.get(n))
            
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

#Run periodically to sense and then send measurements        
    def send(self):
        if len(self.gateway_candidates)> 0:
            self.topK = round(len(self.gateway_candidates)/2)
        else:
            self.topK = len(self.gateways)/2+1
            
        if self.cnt <20:
            sensing_time = datetime.datetime.now()
            reactor.callLater(self.period, self.send)
            self.sense()
            self.cnt +=1
            gatewayTable = self.getRecentGateways(sensing_time)
            gatewayTable = self.removeDuplicates(gatewayTable)
            gatewayTable.extend(self.fillMissingValue(gatewayTable, sensing_time))
            self.categorizeByCapacity(gatewayTable, sensing_time)
            self.selectGateway(gatewayTable)
            neighbors = ""
            for neighbor in self.closeNeighbors:
                neighbors += ','+neighbor            
        else:
            print("END")

####################COSINE SIMILARITY#################
    def square_rooted(self, x): 
        return round(sqrt(sum([a*a for a in x])),3)

    def cosine_similarity(self, x,y):
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        return round(numerator/float(denominator),3)
    
    #Return last measurement round of gateway performances
    def getRecentGateways(self,ts):
        #l = [x for x in self.gatewayTable if (datetime.datetime.now() - self.gatewayTable[x].ts).seconds <= (self.period+10)]
        l = [x for x in self.logs if (datetime.datetime.now()-x.ts).seconds <= (self.period+10)]
        #print(l)
        return l
    
    #Return only last 2 round of measurements of specific gateway
    def get2RecentGateways(self, gateway):
        l = [x for x in self.logs if (datetime.datetime.now() - x.ts).seconds <= (self.period*2) and x.address == gateway.address]
        return l
    
    def getKRecentGateways(self, gateway,k, ts):
        #print("SECONDS",gateway, (self.period*k+10), [x.address for x in self.logs if x.address == gateway])
        l = [x for x in self.logs if (datetime.datetime.now()-x.ts).seconds <= (self.period*k+10) and x.address == gateway]
        l.sort(key=lambda x: x.ts, reverse=False)
        return l
    
##############CATEGORIZING THE GATEWAY NODES###############    
    def getRecentDeviation(self,k, gateway):
        l = [x for x in self.logs if (datetime.datetime.now() - x.ts).seconds <= (self.period*k+10) and x.address == gateway.address]
        if len(l)>0:
            return np.std([x.latency for x in l])
        else:
            return 0
        
    def updateThresholdValues(self):
        self.trshldLat = np.mean([self.gatewayTable[x].latency for x in self.gatewayTable])
        self.trshldDev = np.mean([self.gatewayTable[x].stdev for x in self.gatewayTable])
        
######################SELECTION RELATED FUNCTIONS####################
    def removeDuplicates(self, gateways):
        uniqueGateways = []
        #remove duplicate values
        for gw in gateways:
            for temp in uniqueGateways:
                if gw.address == temp.address and gw.ts>temp.ts:
                    uniqueGateways.remove(temp)
                    break
            uniqueGateways.append(gw)
        return uniqueGateways
        
    def fillMissingValue(self, gateways,ts):
        uniqueGateways = gateways
        returnGWs = []        
        uniqueAddress = [x.address for x in uniqueGateways]
        missingGateways = [x for x in self.gateways if x not in uniqueAddress]
        if len(uniqueGateways) == 0:
            return []
        ts1 = [x.ts for x in uniqueGateways][0]
        #print("Missing gws", missingGateways)
        #Find last 5 measurements from the logs
        for gw1 in missingGateways:
            missingGatewayMeasurements = self.getKRecentGateways(gw1, 5, ts)
            if len(missingGatewayMeasurements)<5:
                continue
            Y = np.array([float(x.latency) for x in missingGatewayMeasurements]).astype(np.float64)
            #X = np.array([x.ts for x in missingGatewayMeasurements]).reshape(-1,1)
            X = np.array([x for x in range(0,len(Y))]).reshape(-1,1)
            model = LinearRegression().fit(X,Y)
            #Predict next 1 measurement
            prediction = model.predict(np.array([x for x in range(len(Y),len(Y)+1)]).reshape(-1,1))
            missingGw = gw.Gateway(ts1, gw1, prediction[0], self.myAddress)
            missingGw = self.setCategory(missingGw)
            #print("predicted",missingGw.address, missingGw.latency)
            returnGWs.append(missingGw)
        return returnGWs
    
    def categorizeByCapacity(self, gateways, ts):
        for gw in gateways:
            #Get last 10 historical values
            gatewayHistories = self.getKRecentGateways(gw.address, 10, ts)
            #print(gw.address, len(gatewayHistories), ":",[x.category for x in gatewayHistories])
            countGood = len([ x for x in gatewayHistories if x.category=="good"])
            countInconsistent = len([ x for x in gatewayHistories if x.category=="inconsistent"])
            countBad = len([ x for x in gatewayHistories if x.category=="bad"])
            if countGood >= countInconsistent and countInconsistent>=countBad:
                gw.capacityCategory = "good"
            elif countGood<countInconsistent and countInconsistent<=countBad:
                gw.capacityCategory = "bad"
            elif countGood<countInconsistent and countInconsistent>countBad and countGood>countBad:
                gw.capacityCategory = "limited"
            elif countGood>countBad and countBad>countInconsistent:
                gw.capacity = "limited"
            else:
                gw.capacityCategory = "inconsistent"        
        candidates = [x.address for x in gateways if x.capacityCategory in ["good", "limited"]]
        print("gateway selection candidates:",candidates)
        self.selection_candidates = candidates
        
    def selectGateway(self, gatewayTable):
        if self.selected_gateway in self.selection_candidates:
            with open('selection_'+self.myAddress,'a') as f:
                f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.selected_gateway))
        else:
            if len(self.selection_candidates) == 0:
                return
            elif len(self.selection_candidates) == 1:
                self.selected_gateway = self.selection_candidates[0]
            else:
                gws = random.sample(set(self.selection_candidates), 2)
                gw1 = [x for x in gatewayTable if x.address == gws[0]][0]
                gw2 = [x for x in gatewayTable if x.address == gws[1]][0]  
                if gw1.latency < gw2.latency:
                    self.selected_gateway = gw1.address
                else:
                    self.selected_gateway = gw2.address            
            with open('selection_'+self.myAddress,'a') as f:
                f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.selected_gateway))
    
    # selecting the best performing gateway from the collaborative gateway performance table
    def selectBestGateway(self, gatewayTable):
        bestGW = ""
        bestLat = 0
        for gw in gatewayTable:
            if bestGW == "":
                bestGW = gw.address
                bestLat = gw.latency
            elif bestLat> gw.latency:
                bestGW = gw.address
                bestLat = gw.latency
        self.selected_gateway = bestGW
        with open('best_'+self.myAddress,'a') as f:
            f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bestGW))
            
     # selecting the best performing gateway from the list of all available gateways
    #client will ping all of them and chose the best one
    def selectAllBestGateway(self):
        bestGW = ""
        bestLat = 0
        perfGws = {}
        for gw in self.gateways:
            lat = self.pingGateway(gw)
            if lat != "":
                perfGws[gw] = lat
        
        for key,value in perfGws.items():            
            if bestGW == "" or bestLat> value:
                bestGW = key
                bestLat = value
            
        self.selected_gateway = bestGW
        with open('best_all_'+self.myAddress,'a') as f:
            f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bestGW))
            
    def senseBest(self):
        if self.cnt <400:
            reactor.callLater(self.period, self.senseBest)
            self.selectAllBestGateway()
            self.cnt+=1
     
    def selectRandomGateway(self, gatewayTable):
        if self.selected_random_gateway not in self.selection_candidates:
            self.selected_gateway = random.sample(set(self.selection_candidates), 1)[0]
        with open('selection_random_'+self.myAddress,'a') as f:
                f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.selected_random_gateway))
            
    
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
        #print('Checking neighbor', node)
        if node == self.myAddress:
            return
        rtt = self.ping(node)
        if rtt < self.trshld:
            self.closeNeighbors.append(node)
            #print('appending',node)
            
    def senseNeighbors(self):
        #print("Sensing neighbors")
        for n in self.neighbors:
            if n == self.myAddress:
                continue
            rtt = self.ping(n)
            if rtt<self.trshld:
                if n not in self.closeNeighbors:
                    self.closeNeighbors.append(n)
        #print("Close neighbors", self.closeNeighbors)

    def senseGateways(self):
        if len(self.gateways)>8:
            return
        #print("Sensing gateways")
        for n in self.originalGateways:
            rtt = self.ping(n)
            #print(n, rtt)
            if rtt != '' and rtt>0 and n not in self.gateways:
                self.gateways.append(n)
                #print('added gateway:', n)
        
##############DOWNLOAD USING SELECTED GATEWAY##################
    def download(self):
        if self.cnt <400:
            reactor.callLater(60, self.download)
            self.downloadContent()
        
    def downloadContent(self):
        ##########Downloading with power of 2 choices################
        status = True
        #cmd='''curl http://'''+self.selected_gateway+''':8080/10Mb.dat -m 180 -w %{time_total},%{http_code} -o /dev/null -s'''
        cmd='''curl -x '''+self.selected_gateway+''':3128 -U david.pinilla:"|Jn 5DJ\\7inbNniK|m@^ja&>C" -m 180 -w %{time_total},%{http_code} http://ovh.net/files/1Mb.dat -o /dev/null -s'''
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')
        if int(code) != 200:
            return
        else:
            with open('download_'+self.myAddress,'a') as f:
                f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(lat.encode('ascii', 'ignore'))))
        