import environments
from environments import Environment
from solver import LaplaceSolver
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

class Exploration:
    def __init__(self, environment):
        self.environment = environment

    def explore(self):
        for x in range(10): #TODO: Impose some condition
            solver = LaplaceSolver(self.environment)
            self.overlayLaplaceSolution()
            solver.findOrdering()
            solver.solve()
            newPos = solver.choosePath()
            self.environment.move(newPos)

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
    e = Exploration(Environment(["XXXXXX", "XOOXOX", "XOOOOX", "XXXXXX"], (1, 1)))
    e.explore()
