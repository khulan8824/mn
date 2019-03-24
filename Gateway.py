
import datetime
import os
import sys

class Gateway:
    address = "" # address of the gateway
    latency = 0.0 # latency TTLB
    ts = None # Last measurement information
    actualLatency = 0.0
    sender = ""

    def __init__(self, address, latency, ts, sender=""):
        self.address = address
        self.latency = latency
        self.actualLatency = latency
        self.ts = ts
        self.sender = sender
        
    
    def printInformation(self):
        print(self.address,':',str(self.latency), ':', str(self.actualLatency),':', self.ts.strftime("%Y-%m-%d %H:%M:%S"),':', self.status)
    