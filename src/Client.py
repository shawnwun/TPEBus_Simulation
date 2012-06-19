import networkx as nx
from random import randrange

class ClientManager:
    # Constructor
    def __init__(self, TPEMap, scoreTable): 
        self._map = TPEMap
        self._table = scoreTable
        self._clients = {}
        self._count = 0
        self._numOfArrived = 0
        self._totalDistance = 0
        self._totalCost = 0
        self._totalBusTransfer = 0
        self._pathCost = nx.all_pairs_dijkstra_path_length(TPEMap,
            None, 'distance')

    def newAllClients(self, graph, numOfClient):
        for i in range(numOfClient):
            start = randrange(1, graph.number_of_nodes() + 1)
            end = start
            while end == start:
                end = randrange(1, graph.number_of_nodes() + 1)
            self._clients[self._count] = Client(
                self._count, start, end, graph)
            self._count += 1
            
    def notifyAllClientsMove(self, graph):
        for cID in self._clients.keys():
            clt = self._clients[cID]
            if clt.isOnNode():
                buses = graph.node[clt.location()]['Buses']
                mindist = self._pathCost[clt.location()][clt.destination()]
                kbest = None
                for k in buses.keys():
                    next = buses[k].nextStop()
                    dist = self._pathCost[next][clt.destination()]
                    if dist < mindist:
                        mindist = dist
                        kbest = k
                if kbest is not None:
                    clt.getOn(graph, buses[kbest])
                # client policy...

    def clearClients(self):
        toDel = []
        for cID in self._clients.keys():
            client = self._clients[cID]
            if client.gotToDestination():
                toDel.append(cID)
        for d in toDel:
            self._totalCost += self._clients[d].lifetime()
            start = self._clients[d].startingPoint()
            end = self._clients[d].destination()
            self._totalDistance += self._pathCost[start][end]
            self._totalBusTransfer += self._clients[d].numOfBusTransfer()
            del self._clients[d]
            self._numOfArrived += 1
            # print 'Clients #%d has arrived and has been removed' % (d)

    def numOfClients(self):
        return len(self._clients)

    def countDown(self):
        for cID in self._clients.keys():
            self._clients[cID].increaseLifetime()

    def totalClientCount(self):
        return self._count

    def numOfArrived(self):
        return self._numOfArrived

    def avgDistance(self):
        return float(self._totalDistance) / self.numOfArrived()

    def avgTimeCost(self):
        return float(self._totalCost) / self.numOfArrived()

    def avgBusTransfer(self):
        return float(self._totalBusTransfer) / self.numOfArrived()

class LocationType:
    NODE, BUS = range(2)

class Client:
    # Constructor
    def __init__(self, id, location, destination, graph):
	self._id = id
        self._start = location
	self._location = location
	self._locationType = LocationType.NODE
	self._destination = destination
	self._lifetime = 0
        self._busTransfer = 0
        self._previousBus = None
        graph.node[self._location]['Clients'][self._id] = self

    def getOn(self, graph, bus):
        bus.clientGetOn(self)
        del graph.node[self._location]['Clients'][self._id]
        self._location = bus.identifier()
        self._locationType = LocationType.BUS
        if self._previousBus is not None:
            if self._location != self._previousBus:
                self._busTransfer += 1
        self._previousBus = self._location
    
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

    def startingPoint(self):
        return self._start
    
    def destination(self):
        return self._destination

    def numOfBusTransfer(self):
        return self._busTransfer

    def lifetime(self):
        return self._lifetime

