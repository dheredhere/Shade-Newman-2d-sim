import environments
from environments import Environment
from collections import deque

class Solver:
    def __init__(self, startEnvironment, startPos):
        self.currentState = startEnvironment
        self.currentPos = startPos
    
    def findOrdering(self):
        ''' 
        finds an ordering of coordinates by distance to the current position
        this is the order we will use to for the jacobi/other iteration
        the ordering is returned in a deque which as a position and depth tuple
        i.e. ((row, col), depth), depth is manhattan distance from start
        '''
        visited = set()
        fringe = deque()
        ordering = deque()

        fringe.append((self.currentPos, 0)) #((row, col), depth)

        while len(fringe) > 0:
            position, depth = fringe.popleft()

            if not position in visited:
                ordering.append((position, depth))
                visited.add(position)

                for neighbor in self.currentState.getNeighbors(position):
                    fringe.append((neighbor, depth + 1))
        return ordering


def getNeighbors(environment, position):
    '''
    finds all valid neighbors from a cell
    returns a list
    '''
    row, col = position
    neighborPositions = [(row+1, col), (row-1, col), 
                         (row, col+1), (row, col-1)]

    #check for out-of-bounds errors and occupied space
    for position in neighborPositions[:]:
        if outOfBounds(position, environment) or environment.isOccupied(position):
            neighborPositions.remove(position)
    return neighborPositions



def test():
    s = Solver(environments.testGridB, (1, 1))
    d = s.findOrdering()
    for i in d:
        print i
        
