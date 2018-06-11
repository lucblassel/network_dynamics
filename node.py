"""
Luc Blassel
Node object of our network
"""

import random as rd

class Node():
    """
    Node of the graph with all the relevant characteristics
    """
    def __init__(self,nodeId,factor,verbose):
        self.id = nodeId
        self.pConnect = rd.random()*factor
        self.pConsult = rd.random()*factor
        self.pLike = rd.random()*factor
        self.pSend = rd.random()*factor
        self.connections = []
        self.visited = False
        self.received = []
        self.consulted = []
        self.liked = []
        self.sent = []
        self.toSend = None #information to send at next timestep
        self.hasLiked = False
        self.hasConsulted = False
        self.verbose = verbose

    def connect(self,nodes):
        """
        creates connections in graph for this node
        it has a pConnect probability to connect to each node in the nodes list
        """
        for node in nodes: #ids
            if node != self.id and node not in self.connections:
                if rd.random() <= self.pConnect:
                    self.connections.append(nodes[node])
                    nodes[node].connections.append(self) #non directed graph

    def receive(self,info):
        """
        handles behaviour of node when recieving an information
        """
        if self.verbose:
            print("node "+str(self.id)+" has received information "+str(info.id))

        if info.id not in self.received:
            self.received.append(info.id)
            if rd.random()<= self.pConsult and info.consultable[self.id][1]:
                self.consult(info)
            else:
                info.consultable[self.id][0] += 1 #not conculted number in increased
        else:
            info.consultable[self.id][0] += 1


    def consult(self,info):
        """
        handles behaviour when info has been consulted
        """
        if self.verbose:
            print("node "+str(self.id)+" has consulted information "+str(info.id))

        self.hasConsulted = True

        self.consulted.append(info.id)
        if rd.random()<= self.pLike:
            self.like(info)

        if rd.random() <= self.pSend:
            self.toSend = info

    def like(self, info):
        """
        handles behaviour when info is liked
        """
        if self.verbose:
            print("node "+str(self.id)+" has liked information "+str(info.id))

        self.hasLiked = True
        self.liked.append(info.id)

    def send(self):
        """
        handles behaviour when sending information
        """
        if self.verbose:
            print("node "+str(self.id)+" sending information "+str(self.toSend.id)+" to it's neighbours.")

        if self.toSend.id not in self.sent:
            self.sent.append(self.toSend.id)
        for node in self.connections:
            node.receive(self.toSend)

        self.toSend = None #resetting value

    def saveNode(self,cursor,netId):
        """
        saves info relevant from node object to local database
        """
        cursor.execute('''INSERT INTO nodes(internalId,pConnect,pSend,pLike,pConsult,networkId) VALUES(?,?,?,?,?,?)''', (self.id,self.pConnect,self.pSend,self.pLike,self.pConsult,netId))

    def saveInteractions(self,cursor,infos,nodes,netId):
        """
        saves all the received, consulted, sent and liked to local database
        """
        received = [(nodes[self.id],infos[i]) for i in self.received]
        consulted = [(nodes[self.id],infos[i]) for i in self.consulted]
        liked = [(nodes[self.id],infos[i]) for i in self.liked]
        sent = [(nodes[self.id],infos[i]) for i in self.sent]

        cursor.executemany('''INSERT INTO received(nodeId, informationId) VALUES (?,?)''',received)
        cursor.executemany('''INSERT INTO consulted(nodeId, informationId) VALUES (?,?)''',consulted)
        cursor.executemany('''INSERT INTO liked(nodeId, informationId) VALUES (?,?)''',liked)
        cursor.executemany('''INSERT INTO sent(nodeId, informationId) VALUES (?,?)''',sent)
