import sys
import os
import operator
from util import *
import networkx as nx
from Bus import *
from Client import *
from random import randrange

# Usage: python src/simulation.py TPMap_nodes.txt TPMap_edges.txt TPMap_traffic.txt TPERoute.txt TPEInterval.txt iteration

NumOfClientsPerMinute = 10

# Build Map
TPEMap = constructMap(sys.argv[1],sys.argv[2],sys.argv[3])
iteration = int(sys.argv[-1])

# Build Bus route information
route = readRoutes(sys.argv[4])
interval = readIntervals(sys.argv[5])

# Table to record the cost
scoreTable = {}

# Initialize Manager, configure it with map and table
bManager = BusManager(TPEMap, scoreTable, route, interval)
cManager = ClientManager(TPEMap, scoreTable)

sum_bus = 0.0
itercnt = 0.0
# Start iteration
for i in range(iteration):
    if i%1000==0:
	print 'iteration %d, # of bus %d, # of client %d' % (i, bManager.numOfBuses(),cManager.numOfClients())
    sum_bus += bManager.numOfBuses()
    itercnt += 1
    if float(i)/float(iteration)<=0.95:
	bManager.newAllBuses(TPEMap)
    if float(i)/float(iteration)<=0.90:
	cManager.newAllClients(TPEMap, randrange(0, NumOfClientsPerMinute + 1))
    
    cManager.notifyAllClientsMove(TPEMap)
    bManager.notifyAllBusesMove(TPEMap)
    cManager.clearClients()
    bManager.countDown()
    cManager.countDown()

# Output Results
# print scoreTable
print
print '=========== Simulation Results =========='
print '--- Client Statistics -------------------'
print '| Clients Generated\t: %d' % (cManager.totalClientCount())
print '| Clients Left on Map\t: %d' % (cManager.totalClientCount()-cManager.numOfArrived())
print '| Completion Rate\t: %.2f %s' % (float(cManager.numOfArrived())*10000.0/float(cManager.totalClientCount())/100.0,'%')
print '| Average Time Cost\t: %.2f min' % (cManager.avgTimeCost())
print '| Expected Travel Dist\t: %.2f m' % (cManager.avgDistance())
print '| Average Stop Transfer\t: %.2f' % (cManager.avgBusTransfer())
print '---- Bus Statistics   -------------------'
print '| Bus Generated\t\t: %d' % (bManager.totalBuses())
print '| Average Bus on Map\t: %d' % (float(sum_bus)/float(itercnt))
print '| Total Travel Dist.\t: %d km' % (bManager.totalDistance()/1000)
#print '---- Overall Measure  -------------------'
#print '| Efficiency\t\t: %.2f ' % (cManager.avgTimeCost()/bManager.totalDistance()*1000000)
print


