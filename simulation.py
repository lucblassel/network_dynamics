"""
Luc Blassel
Dynamic simulation of social network
"""

import sqlite3 as sql
import matplotlib.pyplot as plt
import networkx as nx

from matplotlib import animation
from matplotlib.image import imread
from network import Reseau


class Simulation():
    """
    simulates the flow of information within the network
    """

    def __init__(self,size,forgetTime,disposition,verbose):
        self.network = Reseau(size,disposition,verbose)
        self.forgetTime = forgetTime
        self.verbose = verbose

    def run(self,nTurns):
        """
        runs simulations for a finite number of timesteps
        """
        self.network.initReseau()

        for turn in range(nTurns):
            if self.verbose:
                print(100*'='+'\n\nturn number '+str(turn)+'\n\n'+100*'=')

            self.network.sendAll()
            self.network.selectNode()

            for info in self.network.informations:
                info.checkIfForgotten()
                info.checkLifeSpan()

            self.network.drawFrame() #saves frame for future animation of simulation

        self.animate()

    def printInfo(self):
        for info in self.network.informations:
            print('\n\n')
            print('information number '+str(info.id))
            print(info.consultable)
            print('dead:',info.dead)

    def saveSim(self,dbPath):
        """
        saves all relevant info to local database
        """
        db = sql.connect(dbPath)
        cursor = db.cursor()
        cursor.execute('''INSERT INTO simulations(forgetTime) VALUES(?)''',(self.forgetTime,))
        simId = cursor.lastrowid

        self.network.saveNetwork(cursor,simId) #save baseInfo

        db.commit()
        db.close()

    def animate(self):
        """
        creates and shows animation of previously run simulation
        """
        fig = plt.figure(frameon = False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        frames = []

        for frameNum in range(self.network.frameCount):
            framePath = 'frames/frame'+str(frameNum)+'.png'
            frame = imread(framePath)
            framePlot = plt.imshow(frame)

            frames.append([framePlot])

        anim = animation.ArtistAnimation(fig, frames, interval=300, blit=True, repeat_delay=1000)

        # anim.save("networkSimulation.mp4") #doesn't work 

        plt.show()
def main():
    verbose = False
    dbPath = "networkDynamic.db"
    save = False
    disposition = 'shell' #spring or shell (more spaced out) layout for the graph

    sim = Simulation(20,2,disposition,verbose)
    sim.run(100)
    sim.network.drawReseau()


    if save:
        sim.saveSim(dbPath)

if __name__ == "__main__":
    main()
