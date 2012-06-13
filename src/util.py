import sys
import os
import operator
import networkx as nx


def constructMap(file_name):
    fin = file(file_name,'r')
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
	
	g.add_node(ID,NAME=name,VERGE=isEdge)
	for nei in neighbors:
	    g.add_edge(ID,nei)

    return g

