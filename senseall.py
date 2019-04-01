import random
import sys

from subprocess import check_output, PIPE, Popen
import datetime
import time
import os
import threading
import subprocess
import shlex
from twisted.internet import reactor,protocol

address = str(sys.argv[1])
gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5', '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']

def connectRandom():
    threading.Timer(60, connectRandom).start()
    gwAddress = random.sample(gwAddresses, 2)
    count = 0
    temp = []
    for gw in gwAddresses:
	cmd='''curl http://'''+gw+''':8080/1Mb.dat -m 180 -w %{time_total},%{http_code} -o /dev/null -s'''
	command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')
	with open('logs/logall%s'%(address),'a') as f:
	    f.write("{0},{1},{2},{3}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(gw),str(lat.encode('ascii', 'ignore')), str(address)))


connectRandom()
