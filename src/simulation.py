import sys
import os
import operator
from util import *
import networkx as nx
import Bus
import Client

# Usage: python src/simulation.py TPMap_nodes.txt TPMap_edges.txt TPMap_traffic.txt TPERoute.txt TPEInterval.txt iteration

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

# Start iteration
for i in iteration:
    bManager.notifyAllBusesMove()
    bManager.newAllBuses()
    cManager.newAllClients()
    cManager.notifyAllClientsMove()
    
    bManager.countDown()

# Output Results
print scoreTable

