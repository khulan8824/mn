
import datetime
import os
import sys

class Gateway:
    address = "" # address of the gateway
    latency = 0.0 # latency TTLB
    ts = None # Last measurement information
    actualLatency = 0.0
    sender = ""
    category = "good"
    capacityCategory = "good"

    def __init__(self, ts, address, latency, sender):
        self.address = address
        self.latency = latency
        self.actualLatency = latency
        self.ts = ts
        self.sender = sender
        self.category = "good"
        self.capacityCategory="good"
        self.stdev = 0.0

        
    
    def printInformation(self):
        print(self.address,':',str(self.latency), ':', str(self.actualLatency),':', self.ts.strftime("%Y-%m-%d %H:%M:%S"), ':', self.sender, ':', self.category)
    
