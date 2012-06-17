import networkx as nx
import sys

class BusManager
    
    # Constructor
    def __init__(self, TPEMap, scoreTable, route, interval):
	self._map = TPEMap
	self._score = scoreTable
	self._route = route
	self._interval = interval

	busIDs = self._route.keys()
	buses = {}
	busesCnt = []
	for i in range(len(busIDs)):
	    buses[busID] = []
	    busesCnt.append(0)
	
	self._buses = dict(zip(busIDs,buses))
	self._busesIDCnt = dict(zip(busIDs,busesCnt))
	self._countDown = dict(zip(busIDs,self._interval.values()))

    def notifyAllBusesMove(self, graph):
	for busID in self._buses.keys():
	    buses = self._buses[busID]
	    for bus in buses.values():	
		# Check is parked or not, if is parked, pop it out	
		isParked, stop = bus.isParked()
		if isParked:
		    bus.depark(graph,stop)

		# Start to move
		status, stop, to = bus.move()
		if status==0: # Reach nodes
		    dist = graph.edge[stop][to]['distance']
		    speed = graph.edge[stop][to]['speed']
		    metadata = {'from':stop,'to':to, 'at':0 \
			    'dist':dist, 'speed':speed }
		    self.updateMetadata(metadata)
		    bus.park(graph,stop)
		    bus.getOff(graph,stop)
 
		elif status==-1: # round trip finish, dead
		    


    def newAllBuses(self, graph):
	for busID in self._buses.keys():
	    # if count down == bus interval, generate
	    if(self._countDown[busID]==self._interval[bus]):
		print "Bus route %d # %d is generating..." \
		    % (busID, self._busesIDCnt[busID])
		route = self._route[busID]
		dist = graph.edge[route[0]][route[1]]['distance']
		speed = graph.edge[route[0]][route[1]]['speed']
		metadata = {'from':route[0],'to':route[1], 'at':0 \
			    'dist':dist, 'speed':speed }
		numID = self._busesIDCnt[busID]
		bus = Bus(numID,busID,route,metadata)
		self._buses[busID][numID] = bus


    def countDown(self):

	for busID in self._countDown.keys():
	    
	    # decrease count down table
	    self._countDown[busID] -= 1
	    if self._countDown[busID]==0:
		self_countDown[busID] = self._interval[busID]
	    elif self._countDown[busID]<0:
		print "Bus count down # should not be negative"
		sys.exit()
	    
	    # increase the bus lifetime
	    for buses in self._buses[busID]:
		for bus in buses.values():
		    bus.increaseLifeTime()

class Bus:
    
    # Constructor
    def __init__(self, numID, routeID, route, metadata):
	self.configure(numID, routeID, route, 0)
	self._clients = []
	self._metadata = metadata
	self._isParked = True

    def configure(self, numID, routeID, route, lifetime):
	self._num = numID
	self._route = [routeID, route]
	self._lifetime = lifetime

    def updateMetadata(self, fr, to, at, dist, speed):
	self._metadata['from'] = fr
	self._metadata['to'] = to
	self._metadata['at'] = at
	self._metadata['dist'] = dist
	self._metadata['speed'] = speed

    def increaseLifeTime(self):
	self._lifetime += 1 

    def move(self):
	

    def identifier(self):
	return (self._route[0], self._num)	
    
    def park(self, graph, stop):
	ID = self.identifier()
	graph.node[stop]['Buses'][ID] = self
	isParked = True

    def depark(self, graph, stop):
	ID = self.identifier()
	del graph.node[stop]['Buses'][ID]
	isParked = False

    def isParked(self):
	return isParked, self._metadata['from']

    def clientGetOff(self,stop):
	for c in self._clients():
	    c.getOff(graph,stop)

    def clientGetOn(self,client):
	self._clients.append(client)


