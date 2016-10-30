from environments import Environment
from solver import laplaceSolver

class Exploration:
    def __init__(self, environment, solver):
        self.environment = environment
        self.solver = solver

    def explore(self):
        pass
