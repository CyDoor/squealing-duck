import os
import collections
import platform
import socket, subprocess, sys
import threading
from datetime import datetime
from math import sqrt, ceil

#
# workerThread
#
class workerThread (threading.Thread):
  def __init__(self,threadStart,threadEnd,portStart,portEnd):
    threading.Thread.__init__(self)
    self.threadStart = threadStart
    self.threadEnd = threadEnd
    self.portStart = portStart
    self.portEnd = portEnd
  def run(self):
    if (debug):
      print "workerThread self.threadStart: ",self.threadStart
      print "workerThread self.threadEnd: ",self.threadEnd
      print "workerThread self.portStart: ",self.portStart
      print "workerThread self.portEnd: ",self.portEnd

    for threadIP in xrange(self.threadStart, self.threadEnd + 1):
      networkAddress = networkPrefix + str(threadIP)

      # ARP check here
      # If ARP incomplete skip threadPort loop
      # NOTE TO SELF -> MOVE TO RAW SOCKET FOR ARP AND ARP REPLY RATHER THAN ARP CACHE
      print networkAddress,"Checking ARP."
      tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      socket.setdefaulttimeout(2)
      tcpConnResult = tcpSocket.connect_ex((networkAddress,self.portStart))

      arpCommand = "arp -a | grep " + networkAddress
      if (debug):
        print "workerThread arpCommand: ",arpCommand

      arpResponse = os.popen(arpCommand)
      arpResponseLines = arpResponse.readlines()
      if (debug):
        print "workerThread arpResponse: ",arpResponse
        print "workerThread arpResponse.readLines: ",arpResponseLines

      for arpLine in arpResponseLines:
        if (arpLine.count("incomplete")):
          hostARPed = 0
          if (debug):
            print "workerThread arpLine.count: ",arpLine.count("incomplete")
            print "workerThread hostARPed: ",hostARPed
        else:
          hostARPed = 1
          if (debug):
            print "workerThread arpLine.count: ",arpLine.count("incomplete")
            print "workerThread hostARPed: ",hostARPed
          scanResults[networkAddress,"ARP"] = "LIVE"
          if (debug):
            print "workerThread scanResults: ",networkAddress,scanResults[networkAddress,0]
          break

      if (hostARPed):
        print networkAddress,"ARPed. Scanning ports."
        for threadPort in xrange(self.portStart, self.portEnd + 1):
          tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          socket.setdefaulttimeout(0.5)
          tcpConnResult = tcpSocket.connect_ex((networkAddress,threadPort))

          # If tcp port closed
          if (tcpConnResult):
            tcpSocket.close()
            if (debug):
              print "workerThread",networkAddress,"tcp port",threadPort,"closed"
          # If tcp port open
          else:
            tcpSocket.close()
            if (debug):
              print "workerThread",networkAddress,"tcp port",threadPort,"OPEN"
            scanResults[networkAddress,threadPort] = "OPEN"
        print networkAddress,"Scan Complete"

#Set debug operation
debug = 0
if (debug):
  print "*****************************************************"
  print "******************** DEBUG IS ON ********************"
  print "*****************************************************"


# Get inputs from user
network = raw_input("Enter network: ")
netStart = int(raw_input("Enter starting host: "))
netEnd = int(raw_input("Enter ending host: "))
portStart = int(raw_input("Enter starting port: "))
portEnd = int(raw_input("Enter ending port: "))
networkSplits = network.split('.')
networkPrefix = networkSplits[0] + '.' + networkSplits[1] + '.' + networkSplits[2] + '.'
startTime = datetime.now()
scanResults = collections.OrderedDict()

if (debug):
  print "Main network: ", network
  print "Main netStart: ", netStart
  print "Main netEnd: ", netEnd
  print "Main networkPrefix: ", networkPrefix
  print "Main portStart: ", portStart
  print "Main portEnd: ", portEnd

print "Start Time: ", startTime

# Get OS and form ping command string
oper = platform.system()

if (oper == "Windows"):
  pingCmd = "ping -n 1 "
elif (oper == "Linux"):
  pingCmd = "ping -c 1 "
else:
  pingCmd = "ping -c 1 "

if (debug):
  print "Main pingCmd: ", pingCmd

# Determine number of threads and IP ranges in each thread
totalIPs = netEnd - netStart + 1
totalThreads = int(ceil(sqrt(totalIPs)))

if (totalIPs % totalThreads) > 0:
  numPerThread = int(ceil(totalIPs/totalThreads)) + 1
else:
  numPerThread = int(ceil(totalIPs/totalThreads))

if (debug):
  print "Main totalIPs: ", totalIPs
  print "Main totalThreads: ", totalThreads
  print "Main numPerThread: ", numPerThread

# Initialize threads array
threads=[]

# Start each thread
try:
  for threadIndex in xrange(totalThreads):
    
    threadStart = (threadIndex * numPerThread) + 1
    threadEnd = (threadIndex * numPerThread) + numPerThread

    if (threadEnd > netEnd):
      threadEnd = netEnd

    if (debug):
      print "Main threadIndex: ", threadIndex
      print "Main threadStart: ", threadStart
      print "Main threadEnd: ", threadEnd

    thread = workerThread(threadStart,threadEnd,portStart,portEnd)
    thread.start()
    threads.append(thread)
except:
  print "**************************"
  print "***** Thread failure *****"
  print "**************************"

# Wait for all threads to finish
for t in threads:
  t.join()

# Sorting and printing results
endTime = datetime.now()
print "End Time: ", endTime

collections.OrderedDict(sorted(scanResults.items()))

for netAddress,port in scanResults:
  print netAddress,"tcp port",port,scanResults[netAddress,port]

print "COMPLETE in: ", endTime - startTime
