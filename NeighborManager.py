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

class NeighborManager:
    neighborAddress= ""
    neighbors = []
    closeNeighbors = []
    gateways = []
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
        #print(cmd)
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')
        #print(lat, code)
        if int(code) != 200:
            return ""
        else:
            with open('log','a') as f:
                f.write("{0},{1},{2},{3},{4}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(address),str(lat), str(self.myAddress), str(self.myAddress)))
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+','+str(address)+","+str(lat)+","+self.myAddress
        #print('gw', address, ' lat', lat)
    
    def sense(self):
        gws = self.select2Random()
        txt = ""
        for gw in gws:
            t = self.pingGateway(gw)
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