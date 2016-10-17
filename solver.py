import environments
from environments import Environment
from collections import deque
import numpy as np  
from copy import deepcopy

class LaplaceSolver:
    def __init__(self, startEnvironment, startPos):
        self.currentState = startEnvironment
        self.currentPos = startPos
        self.ordering = deque()

        #init approximation matrix with same dims as grid
        #fill with 0's, 1 at start position
        self.approximation = np.zeros_like(startEnvironment.grid)
        row, col = startPos
        self.approximation[row][col] = 1
    
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

        #fringe.append((self.currentPos, 0)) #((row, col), depth)
        visited.add(self.currentPos) #dont want to expand start (always 1)
        #add the neighbors of the start vertex to the queue
        for neighbor in self.currentState.getNeighbors(self.currentPos):
            fringe.append((neighbor, 1))

        while len(fringe) > 0:
            position, depth = fringe.popleft()

            if not position in visited:
                ordering.append((position, depth))
                visited.add(position)

                for neighbor in self.currentState.getNeighbors(position):
                    fringe.append((neighbor, depth + 1))
        self.ordering = ordering
        return ordering

    def timeStep(self):
        '''
        find an ordering and compute 1 step of the Gauss-Seidel method
        '''
        self.findOrdering()
        for (cell, depth) in self.ordering:
            rowNeighbors = self.currentState.getRowNeighbors(cell)
            colNeighbors = self.currentState.getColNeighbors(cell)
            #print 'cell: ' + str(cell) + '\nrow: ' + str(rowNeighbors) + "\ncol: " + str(colNeighbors)
            make row and col neighbor lists even to remove cases
            rowNeighbors = useSymmetry(rowNeighbors)
            colNeighbors = useSymmetry(colNeighbors)
            print "current pos: " + str(cell)
            print "row: " + str(rowNeighbors)
            print "col: " + str(colNeighbors)
            neighbors = rowNeighbors + colNeighbors

            #then average neighbor values to find value for current cell
            neighborSum = 0
            for neighbor in neighbors:
                row, col = neighbor
                neighborSum += self.approximation[row][col]
            updatedValue = neighborSum/len(neighbors)
            
            #update current cell
            row, col = cell
            self.approximation[row][col] = updatedValue

#very basic, just to verify changes
#remove later

def useSymmetry(neighbors):
    '''
    makes the list even so averaging neighbors is easier
    '''
    if len(neighbors) == 1:
        neighbor = deepcopy(neighbors[0])
        neighbors.append(neighbor)
        return neighbors

    return neighbors

def test():
    s = LaplaceSolver(environments.testGridB, (1, 1))
    s.currentState.display()
    print s.findOrdering()
    s.timeStep()
    print s.approximation
    return s
        
