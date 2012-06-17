import sys
import os
import operator
import networkx as nx


def constructMap(nodefile,edgefile,trfffile):

    dist = readDistance(edgefile)
    trff = readTraffic(trfffile)

    fin = file(nodefile,'r')
    line = fin.readline()
    g = nx.Graph()    
    for line in fin.readlines():
	tokens = line.replace('\n','').split('\t')
	
	ID = int(tokens[0])
	name = tokens[1]
	isEdge = False
	if tokens[3]=='Y':
	    isEdge = True
	neighbors = [int(n) for n in tokens[-1].split(';')]
	
	g.add_node(ID,NAME=name,VERGE=isEdge,Clients=[],Buses={})
	for nei in neighbors:
	    tup = tuple(sorted([ID,nei]))
	    g.add_edge(ID,nei,distance=dist[tup],speed=trff[tup])

    fin.close()
    return g


def readRoutes(filename):
    fin = file(filename,'r')
    routes = {}
    for line in fin.readlines():
	pair = line.replace('\n','').split()
	routes[int(pair[0])] = [int(n) for n in pair[-1].split(';')]
    fin.close()
    return routes

def readDistance(filename):
    fin = file(filename,'r')
    distance = {}
    for line in fin.readlines():
	tokens = line.replace('\n','').split()
	distance[(int(tokens[0]),int(tokens[1]))] = int(tokens[-1])
    fin.close()
    return distance

def readTraffic(filename):
    fin = file(filename,'r')
    traffic = {}
    for line in fin.readlines():
	tokens = line.replace('\n','').split()
	traffic[(int(tokens[0]),int(tokens[1]))] = int(tokens[-1])
    fin.close()
    return traffic

def readIntervals(filename):
    fin = file(filename,'r')
    interval = {}
    for line in fin.readlines():
	pair = [int(p) for p in line.split()]
	interval[pair[0]] = pair[1]
    fin.close()
    return interval

