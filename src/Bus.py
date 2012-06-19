import networkx as nx
import sys

class BusManager:
    
    # Constructor
    def __init__(self, TPEMap, scoreTable, route, interval):
	self._map = TPEMap
	self._score = scoreTable
	self._route = route
	self._interval = interval
	self._totalBus = 0;
	self._totalDistance = 0;

	busIDs = self._route.keys()
	buses = []
	busesCnt = []
	for i in range(len(busIDs)):
	    buses.append({})
	    busesCnt.append(0)
	
	self._buses = dict(zip(busIDs,buses))
	self._busesIDCnt = dict(zip(busIDs,busesCnt))
	self._countDown = dict(zip(busIDs,self._interval.values()))

    def collectAllBusScore(self):
	pass

    def totalDistance(self):
	return self._totalDistance

    def numOfBuses(self):
	cnt = 0
	for busID in self._buses.keys():
	    cnt += len(self._buses[busID])
	return cnt

    def notifyAllBusesMove(self, graph):
	for busID in self._buses.keys():
	    
	    for num in self._buses[busID].keys():	
		# Check is parked or not, if is parked, pop it out	
		bus = self._buses[busID][num]
		isParked, stop = bus.isParked()
		if isParked:
		    bus.depark(graph,stop)

		# Start to move
		status, stop, to = bus.move()
		if status==0: # Reach nodes
		    dist = graph.edge[stop][to]['distance']
		    speed = graph.edge[stop][to]['speed']
		    metadata = {'from':stop, 'to':to, 'at':0, 'dist':dist, 'speed':speed }
		    bus.updateMetadata(metadata)
		    bus.park(graph,stop)
		    bus.clientGetOff(graph,stop)
 
		elif status==-1: # round trip finish, dead    
		    bus.clientGetOff(graph,stop) 
		    self._score[bus.identifier()] = bus.getDistance()
		    self._totalDistance += bus.getDistance()
		    del self._buses[busID][num]
		    #if busID==14:
		    #	print self._buses[busID]
			#print bus._metadata
    
    def newAllBuses(self, graph):
	for busID in self._buses.keys():
	    # if count down == bus interval, generate
	    if(self._countDown[busID]==self._interval[busID]):
		#print "Bus route %d # %d is generating..." \
		#    % (busID, self._busesIDCnt[busID])
		route = self._route[busID]
		dist = graph.edge[route[0]][route[1]]['distance']
		speed = graph.edge[route[0]][route[1]]['speed']
		metadata = {'from':route[0], 'to':route[1],
                    'at':0, 'dist':dist, 'speed':speed }
		numID = self._busesIDCnt[busID]
		bus = Bus(numID,busID,route,metadata)
		self._buses[busID][numID] = bus
		bus.park(graph,route[0])
		self._busesIDCnt[busID] += 1
		self._totalBus += 1

    def totalBuses(self):
	return self._totalBus
    
    def countDown(self):
	for busID in self._countDown.keys():
	    
	    # decrease count down table
	    self._countDown[busID] -= 1
	    if self._countDown[busID]==0:
		self._countDown[busID] = self._interval[busID]
	    elif self._countDown[busID]<0:
		print "Bus count down # should not be negative"
		sys.exit()
	    
	    # increase the bus lifetime
	    for bus in self._buses[busID].values():
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
	self._distance = 0

    def updateMetadata(self, meta):
	del self._metadata
	self._metadata = meta

    def nextStop(self):
        return self._metadata['to']

    def increaseLifeTime(self):
	self._lifetime += 1 

    def increaseDistance(self,dist):
	self._distance += dist

    def move(self):
	status = 1
	self._metadata['at'] += self._metadata['speed']
	self.increaseDistance(self._metadata['speed'])
	newFrom = self._metadata['from']
	newTo = self._metadata['to']

	if self._metadata['at']>=self._metadata['dist']:#reach nodes
	    status = 0
	    fromIdx = self._route[1].index(self._metadata['from'])
	    toIdx = self._route[1].index(self._metadata['to'])
	    if fromIdx>toIdx: # reverse
		if toIdx==0: # reach back to begin
		    newFrom = self._route[1][fromIdx-1]
		    newTo = self._route[1][toIdx]
		else:
		    newFrom = self._route[1][fromIdx-1]
		    newTo = self._route[1][toIdx-1]
	    elif fromIdx<toIdx: # no reverse
		if toIdx==len(self._route[1])-1:
		    newFrom = self._route[1][toIdx]
		    newTo = self._route[1][fromIdx]
		else:
		    newFrom = self._route[1][fromIdx+1]
		    newTo = self._route[1][toIdx+1]
	    else:
		print "Error, from , to index error in bus!!"
	    if self._metadata['to']==self._route[1][0]:# end
		status = -1
		
	return status, newFrom, newTo 

    def identifier(self):
	return (self._route[0], self._num, 'bus')	
    
    def park(self, graph, stop):
	ID = self.identifier()
	graph.node[stop]['Buses'][ID] = self
	self._isParked = True

    def depark(self, graph, stop):
	ID = self.identifier()
	del graph.node[stop]['Buses'][ID]
	self._isParked = False

    def isParked(self):
	return self._isParked, self._metadata['from']

    def clientGetOff(self,graph,stop):
	for c in range(len(self._clients)):
	    self._clients[c].getOff(graph,stop)
        del self._clients[:]
    def clientGetOn(self,client):
	self._clients.append(client)
	
    def getLifeTime(self):
	return self._lifetime

    def getDistance(self):
	return self._distance



