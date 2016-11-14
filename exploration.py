import environments
from collections import deque
from environments import Environment, genEnvStrings, selectRandomStart
from solver import LaplaceSolver
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

class Explorer:
    def __init__(self, environment):
        self.environment = environment

    def explore(self):
        steps = 0
        while self.environment.howManyUnexplored() > 2: 
            solver = LaplaceSolver(self.environment)
            #print self.fullyExplored()
            self.overlayLaplaceSolution()
            solver.findOrdering()
            solver.solve()
            newPos = solver.choosePath()

            #if wants to move to an occupied position,
            #rescan and try to move to unoccupied space
            '''
            while self.environment.isOccupied(newPos):
                self.environment.move(self.environment.currentPos)
                solver = LaplaceSolver(self.environment)
                self.overlayLaplaceSolution()
                solver.findOrdering()
                solver.solve()
            '''

            self.environment.move(newPos)
            steps += 1

        self.overlayLaplaceSolution()
        
    def fullyExplored(self):
        '''
        runs bfs on currentState of environment
        terminates at occupied cells
        returns true if there are still unexplored cells
        '''
        visited = set()
        fringe = deque()
        ordering = deque()

        visited.add(self.environment.currentPos)
        neighbors = self.environment.getAllNeighbors(self.environment.currentPos)
        for neighbor in neighbors:
            fringe.append(neighbor)

        while len(fringe) > 0:
            cell = fringe.popleft()

            if (self.environment.isUnexplored(cell)):
                return False
            elif not cell in visited and not self.environment.isOccupied(cell):
                visited.add(cell)

                neighbors = self.environment.getAllNeighbors(cell)
                for neighbor in neighbors:
                    fringe.append(neighbor)

        return True

    def overlayLaplaceSolution(self):
        cmap = mpl.colors.ListedColormap(['black', 'purple', 'white', 'green'])
        bounds = [-2, -.0001, .0001, 2, 12]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        
        x, y = self.environment.currentPos
        value = self.environment.currentState[x][y]
        self.environment.currentState[x][y] = 10
        
        img = plt.imshow(self.environment.currentState, interpolation='nearest', cmap = cmap, norm=norm)
        plt.colorbar(img, cmap=cmap, norm=norm, boundaries = bounds, ticks=[-1,0,1])
        plt.show()

        self.environment.currentState[x][y] = value

def test():
    envStrings = genEnvStrings(20, 10, 10)
    env = Environment(envStrings, selectRandomStart(envStrings))
    e = Explorer(env)
    e.explore()
