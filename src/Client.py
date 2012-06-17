import networkx as nx
from random import randrange

class LocationType
    NODE, BUS = range(2)

class ClientManager
    # Constructor
    def __init__(self, TPEMap, scoreTable, bManager): 
	self._map = TPEMap
	self._table = scoreTable
	self._clients = {}
        self._count = 0
        self._busManager = bManager

    def newAllClients(self, numOfClient):
	for i in range(numOfClient):
            self._clients[self._count] = Client(
                self._count,
                randrange(0, self._map.number_of_nodes() ),
                randrange(0, self._map.number_of_nodes() ),
                self._busManager )
            self._count += 1
            
    def notifyAllClientsMove(self):
	for key in self._clients.keys()
            clients[key].move()

    def numOfClients(self):
        return len(self._clients)

class Client
    # Constructor
    def __init__(self, id, location, destination, bManager):
	self._id = id
	self._location = location
	self._location_type = LocationType.NODE
	self._destination = destination
	self._lifetime = 0
        self._busManager = bManager
    
    def move(self):

    def getOn(self, busID):
        self._busManager._buses[busID].clientGetOn(self._id)
        self._location = busID
        self._location_type = LocationType.BUS
    
    def getOff(self, graph, stop)
        self._location = stop


