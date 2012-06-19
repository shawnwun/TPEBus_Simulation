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
            self._clients[self._count] = Client(
                self._count,
                randrange(0, self._map.number_of_nodes() ),
                randrange(0, self._map.number_of_nodes() ),
                graph )
            self._count += 1
            
    def notifyAllClientsMove(self, graph):
        toDel = []
        for cID in self._clients.keys():
            client = self._clients[cID]
            if client.gotToDestination():
                toDel.append(cID)
        for d in toDel:
            del self._clients[cID]
            print 'Clients #%d has arrived and has been removed' % (cID)

        for cID in self._clients.keys():
            client = self._clients[cID]
            if client.isOnNode():
                buses = graph.node[client.location()]['Buses']
                # TODO

    def numOfClients(self):
        return len(self._clients)

    def countDown(self):
        for cID in self._clients.keys():
            self._clients[cID].addLifetime()

class Client:
    class LocationType:
        NODE, BUS = range(2)
    # Constructor
    def __init__(self, id, location, destination, graph):
	self._id = id
	self._location = location
	self._locationType = LocationType.NODE
	self._destination = destination
	self._lifetime = 0
        graph.node[stop]['Clients'][self._id] = self

    def getOn(self, graph, bus):
        bus.clientGetOn(self)
        self._location = bus.identifier()
        self._locationType = LocationType.BUS
        del graph.node[stop]['Clients'][self._id]
    
    def getOff(self, graph, stop):
        self._location = stop
        self._locationType = LocationType.NODE
        graph.node[stop]['Clients'][self._id] = self

    def identifier(self):
        return self._id

    def addLifetime(self):
        self._lifetime += 1

    def isOnBus(self):
        return self._locationType == LocationType.BUS

    def isOnNode(self):
        return self._locationType == LocationType.NODE

    def gotToDestination(self):
        return self.isOnNode() and self._location == self._destination

    def location(self):
        return self._location

