import sys
import os
import operator
from util import *
import networkx as nx
from Bus import *
from Client import *

# Usage: python src/simulation.py TPMap_nodes.txt TPMap_edges.txt TPMap_traffic.txt TPERoute.txt TPEInterval.txt iteration scenario

# scenrio : 'morning', 'evening', 'offpeak'

NumOfClientsPerMinute = 30

# Build Map
TPEMap = constructMap(sys.argv[1],sys.argv[2],sys.argv[3])
iteration = int(sys.argv[6])
scenario = sys.argv[-1]

# Build Bus route information
route = readRoutes(sys.argv[4])
interval = readIntervals(sys.argv[5])

# Table to record the cost
scoreTable = {}

# Initialize Manager, configure it with map and table
bManager = BusManager(TPEMap, scoreTable, route, interval)
cManager = ClientManager(TPEMap, scoreTable)

# Start iteration
for i in range(iteration):
    if i%1000==0:
	print 'iteration %d, # of bus %d, # of client %d' % (i, bManager.numOfBuses(),cManager.numOfClients())
    bManager.newAllBuses(TPEMap)
    cManager.newAllClients(TPEMap, NumOfClientsPerMinute, scenario)
    cManager.notifyAllClientsMove(TPEMap)
    bManager.notifyAllBusesMove(TPEMap)
    cManager.clearClients()
    bManager.countDown()
    cManager.countDown()

# Output Results
# print scoreTable
print 'Total # of clients: %d' % (cManager.totalClientCount())
print '# of clients arrived: %d' % (cManager.numOfArrived())
print 'Average expected traveling distance: %.2f' % (cManager.avgDistance())
print 'Average time cost: %.2f' % (cManager.avgTimeCost())
print 'Average # of bus transfers: %.2f' % (cManager.avgBusTransfer())
