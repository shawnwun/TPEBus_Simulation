import networkx as nx
from random import randrange

class ClientManager:
    # Constructor
    def __init__(self, TPEMap, scoreTable): 
        self._map = TPEMap
        self._table = scoreTable
        self._clients = {}
        self._count = 0

    def newAllClients(self, graph, numOfClient):
        for i in range(numOfClient):
            start = randrange(1, self._map.number_of_nodes() + 1)
            end = start
            while end == start:
                end = randrange(1, self._map.number_of_nodes() + 1)
            self._clients[self._count] = Client(
                self._count, start, end, graph)
            self._count += 1
            
    def notifyAllClientsMove(self, graph):
        toDel = []
        for cID in self._clients.keys():
            client = self._clients[cID]
            if client.gotToDestination():
                toDel.append(cID)
        for d in toDel:
            del self._clients[d]
            print 'Clients #%d has arrived and has been removed' % (d)

        for cID in self._clients.keys():
            client = self._clients[cID]
            if client.isOnNode():
                buses = graph.node[client.location()]['Buses']
                for k in buses.keys():
                    client.getOn(graph, buses[k])
                    break
                # TODO

    def numOfClients(self):
        return len(self._clients)

    def countDown(self):
        for cID in self._clients.keys():
            self._clients[cID].increaseLifetime()

class LocationType:
    NODE, BUS = range(2)

class Client:
    # Constructor
    def __init__(self, id, location, destination, graph):
	self._id = id
	self._location = location
	self._locationType = LocationType.NODE
	self._destination = destination
	self._lifetime = 0
        graph.node[self._location]['Clients'][self._id] = self

    def getOn(self, graph, bus):
        bus.clientGetOn(self)
        del graph.node[self._location]['Clients'][self._id]
        self._location = bus.identifier()
        self._locationType = LocationType.BUS
    
    def getOff(self, graph, stop):
        self._location = stop
        self._locationType = LocationType.NODE
        graph.node[stop]['Clients'][self._id] = self

    def identifier(self):
        return self._id

    def increaseLifetime(self):
        self._lifetime += 1

    def isOnBus(self):
        return self._locationType == LocationType.BUS

    def isOnNode(self):
        return self._locationType == LocationType.NODE

    def gotToDestination(self):
        return self.isOnNode() and self._location == self._destination

    def location(self):
        return self._location

