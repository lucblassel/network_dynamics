"""
Luc Blassel

Info object used for network simulation
"""

class Info():
    """
    information with an id and a  life (time steps spent in the network)
    """
    def __init__(self, idInfo, forgetTime, nodes, verbose):
        self.id = idInfo
        self.lifeSpan = 1
        self.forgetTime = forgetTime
        self.consultable = {node:[0,True] for node in nodes} #for each node, number it has been recieved but not consulted, and consultable
        self.dead = False
        self.verbose = verbose

    def checkIfForgotten(self):
        """
        checks if the information has been forgotten for each node
        """
        for key in self.consultable:
            if self.consultable[key][0] >= self.forgetTime:
                self.consultable[key][1] = False

    def checkLifeSpan(self):
        """
        checks if information is still alive
        """
        if not self.dead:
            alive = False
            for key in self.consultable:
                if self.consultable[key][1]:
                    alive = True
            if alive:
                self.lifeSpan += 1
            else:
                if self.verbose:
                    print("information "+str(self.id)+" has died after a life of "+str(self.lifeSpan))
                self.dead = True

    def saveInfo(self,cursor,netId):
        """
        saves relevant info to local database
        """
        deathValue = 1 if self.dead else 0

        cursor.execute('''INSERT INTO informations(internalId,networkId,dead) VALUES(?,?,?)''',(self.id,netId,deathValue))
        infoId = cursor.lastrowid

        consultables = []
        for node in self.consultable:
            cursor.execute(''' SELECT nodeId FROM nodes WHERE internalId = ? AND networkId = ?''',(node,netId))
            globalId = cursor.fetchone()[0]
            consultables.append((infoId, globalId, self.dead))

        cursor.executemany('''INSERT INTO consultables(informationId,nodeId,value) VALUES(?,?,?)''',consultables )
