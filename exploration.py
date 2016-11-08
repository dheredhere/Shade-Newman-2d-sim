from environments import Environment
from solver import LaplaceSolver

class Exploration:
    def __init__(self, environment, solver):
        self.environment = environment
        self.solver = solver

    def explore(self):
        while(1): #TODO: Impose some condition
            solver.findOrdering()
            solver.solve()
            solver.choosePath()
