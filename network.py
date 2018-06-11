"""
Luc Blassel
network object
"""

import networkx as nx
import matplotlib.pyplot as plt
import random as rd

from queue import Queue
from node import Node
from info import Info

class Reseau():
    """
    Network of nodes
    """
    def __init__(self,size,disposition,verbose):
        if size <2:
            print("A network must contain at least 2 nodes...")
            return
        self.size = size
        self.nodes = {}
        self.informations = []
        self.verbose = verbose
        self.frameCount = 0
        self.edges = []
        self.layout = None
        self.dispo = nx.layout.spring_layout if disposition == 'spring' else nx.layout.shell_layout
        self.draw = nx.draw_spring if disposition == 'spring' else nx.draw_shell

    def initReseau(self):
        """
        initializes nodes and connections in graph
        """
        self.nodes = {i:Node(i,0.3,self.verbose) for i in range(self.size)}
        for i in self.nodes:
            self.nodes[i].connect(self.nodes)

    def drawReseau(self):
        """
        draws the network with networkX instead of graphviz
        """
        G = nx.Graph()
        G.add_nodes_from(self.nodes.keys())

        edges = []
        for key in self.nodes:
            node = self.nodes[key]
            for dest in node.connections:
                edge = [key,dest.id]
                edge.sort()
                edge = tuple(edge)
                edges.append(edge)
        edges = set(edges)

        G.add_edges_from(edges)

        self.draw(G, with_labels=True, font_weight='bold')
        plt.show()

    def drawFrame(self):
        """
        draws frame of animation to see the evolution of network
        """
        G = nx.Graph()

        edges = []
        for key in self.nodes:
            node = self.nodes[key]
            color = 'r'
            shape = 'o'

            if node.hasLiked :
                color = 'g'
            if node.hasConsulted:
                shape = 's'

            G.add_node(node.id,shape = shape, color = color)
            if not self.edges:
                for dest in node.connections:
                    edge = [key,dest.id]
                    edge.sort()
                    edge = tuple(edge)
                    edges.append(edge)

        if not self.edges: #dont find edges at each frame, find them once and save them
            edges = set(edges)
            self.edges = edges

        for edge in self.edges:
            if self.nodes[edge[0]].toSend is not None or self.nodes[edge[1]].toSend is not None : #either one of the nodes are sending info
                G.add_edge(edge[0], edge[1], color = 'b', weight = 4)
            else:
                G.add_edge(edge[0], edge[1], color = 'k', weight = 2)

        # G.add_edges_from(self.edges)
        edgeColors = [G[u][v]['color'] for u,v in G.edges()]
        edgeWeights = [G[u][v]['weight'] for u,v in G.edges()]

        if self.layout is None:
            nodePos = self.dispo(G)
            self.layout = nodePos
        else: #to keep nodes in same place during iterations
            nodePos = self.layout

        nodeShapes = set((aShape[1]["shape"] for aShape in G.nodes(data = True)))

        fig = plt.figure(frameon = False)
        fig.suptitle('step '+str(self.frameCount))
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        for shape in nodeShapes:
            nodeList = [sNode[0] for sNode in filter(lambda x: x[1]["shape"] == shape,G.nodes(data = True))]
            colorList = [sNode[1]["color"] for sNode in filter(lambda x: x[1]["shape"] == shape,G.nodes(data = True))]
            nx.draw_networkx_nodes(G,nodePos,node_shape = shape, node_color = colorList , nodelist = nodeList)

        nx.draw_networkx_edges(G, nodePos, width = edgeWeights, edge_color = edgeColors )
        nx.draw_networkx_labels(G, pos = nodePos)

        fig.savefig('frames/frame'+str(self.frameCount)+'.png', dpi = 200)
        plt.close()
        self.frameCount += 1

    def breadthFirst(self,node,node2):
        """
        breadth first search of graph starting from node, returns shortest path to node2
        """
        queue = Queue(maxsize=len(self.nodes))
        queue.put(self.nodes[node])
        self.nodes[node].visited = True

        path = []
        prev = {}
        prev[node]=None

        if node == node2:
            return

        while not queue.empty():
            node = queue.get()
            # print(node.id)
            for neighbour in node.connections:
                neighbour = neighbour.id
                if not self.nodes[neighbour].visited:
                    prev[neighbour] = node.id
                    queue.put(self.nodes[neighbour])
                    self.nodes[neighbour].visited = True
                    if neighbour == node2:
                        prevNode = node.id
                        path.append(neighbour)
                        while prevNode is not None:
                            path.append(prevNode)
                            prevNode = prev[prevNode]
                        path.reverse()
                        return path

    def resetNodes(self):
        """
        resets visited status of all nodes in network
        """
        for node in self.nodes:
            self.nodes[node].visited = False

    def distance(self,node1,node2):
        """
        returns minimum distance between 2 nodes
        """
        path = self.breadthFirst(node1,node2)
        return len(path)-1 if path is not None else None

    def diametre(self):
        """
        returns maximum possible distance between 2 nodes
        """
        maxDist = 0
        for node1 in range(len(self.nodes)):
            for node2 in range(node1+1,len(self.nodes)): #no need to go through all nodes (bc. distance is symetrical)
                self.resetNodes()
                dist = self.distance(node1,node2)
                if dist is not None and dist > maxDist:
                    maxDist = dist
        return maxDist

    def selectNode(self):
        """
        selects a random node in the network and has it send a new information
        """
        chosenNode = rd.choice(list(self.nodes.keys()))
        self.introduceInfo()
        self.nodes[chosenNode].toSend = self.informations[-1]
        self.nodes[chosenNode].send()

    def introduceInfo(self):
        """
        creates an information in the network
        """

        if not self.informations:
            infoId = 0
        else:
            infoId = self.informations[-1].id+1

        if self.verbose:
            print("introducing information number "+str(infoId))

        self.informations.append(Info(infoId,2,self.nodes.keys(),self.verbose))

    def sendAll(self):
        """
        send all information to send at the beginning of each timestep
        """
        for node in self.nodes:
            if self.nodes[node].toSend is not None:
                self.nodes[node].send()
            self.nodes[node].hasLiked = False
            self.nodes[node].hasConsulted = False #to animate graph

    def getConnections(self,netId):
        """
        gets all unique connections in graph
        """
        connections = []
        for key in self.nodes:
            node = self.nodes[key]
            for dest in node.connections:
                connection = [key,dest.id]
                connection.sort()
                connection = [netId] + connection
                connection = tuple(connection)
                connections.append(connection)
        return connections

    def getInfos(self,cursor,netId):
        """
        get global informations id from local database
        """
        cursor.execute('''SELECT informationId, internalId FROM informations WHERE networkId = ?''',(netId,))

        infos = {}
        for row in cursor:
            infos[row[1]] = row[0]

        return infos

    def getNodes(self,cursor,netId):
        """
        get global node id from local database
        """
        cursor.execute('''SELECT nodeId, internalId FROM nodes WHERE networkId = ?''',(netId,))

        nodes = {}
        for row in cursor:
            nodes[row[1]] = row[0]

        return nodes

    def saveNetwork(self,cursor,simId):
        """
        saves relevant network info to local database
        """
        cursor.execute('''INSERT INTO networks(networkId,size,simulationId) VALUES(?,?,?)''',(simId,self.size,simId))

        for node in self.nodes:
            self.nodes[node].saveNode(cursor,simId)
        for info in self.informations:
            info.saveInfo(cursor,simId)

        connections = self.getConnections(simId)
        cursor.executemany('''INSERT INTO connections(networkId,startNode,endNode) VALUES(?,?,?)''',connections)

        infoIds = self.getInfos(cursor,simId)
        nodeIds = self.getNodes(cursor,simId)

        for node in self.nodes:
            self.nodes[node].saveInteractions(cursor,infoIds,nodeIds,simId)


def main():
    net = Reseau(10)
    net.initReseau()
    print('distance',net.distance(1,4))
    print('diameter',net.diametre())
    print(net.getConnections(1))
    net.drawReseau()

if __name__ == '__main__':
    main()
