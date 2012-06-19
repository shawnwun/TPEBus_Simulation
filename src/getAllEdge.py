import os
import sys
import operator
from util import *
import matplotlib.pyplot as plt

fname = sys.argv[1]
edge = sys.argv[2]
trff = sys.argv[3]

g = constructMap(fname,edge,trff)

for e in g.edges():
    print e[0],e[1],g.node[e[0]]['NAME'],g.node[e[1]]['NAME']

nx.draw(g)
plt.show()

