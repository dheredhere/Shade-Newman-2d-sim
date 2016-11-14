import environments
from environments import Environment
from collections import deque
import numpy as np  
from copy import deepcopy
import pylab as plt

class LaplaceSolver:
    def __init__(self, startEnvironment):
        self.currentState = startEnvironment
        self.currentPos = startEnvironment.currentPos
        self.ordering = deque()

        #init approximation matrix with same dims as grid
        #fill with 0's, 1 at start position
        self.approximation = np.zeros_like(startEnvironment.currentState)
        row, col = self.currentPos
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
        #self.findOrdering()
        for (cell, depth) in self.ordering:
            rowNeighbors = self.currentState.getRowNeighbors(cell)
            colNeighbors = self.currentState.getColNeighbors(cell)
        
            #make row and col neighbor lists even to remove cases
            rowNeighbors = useSymmetry(rowNeighbors)
            colNeighbors = useSymmetry(colNeighbors)
            '''
            print "current pos: " + str(cell)
            print "row: " + str(rowNeighbors)
            print "col: " + str(colNeighbors)
            '''
            neighbors = rowNeighbors + colNeighbors

            #then average neighbor values to find value for current cell
            neighborSum = 0
            for neighbor in neighbors:
                row, col = neighbor
                neighborSum += self.approximation[row][col]
            length = len(neighbors)
            if (length == 0):
                length = 1
            updatedValue = neighborSum/length
            
            #update current cell
            row, col = cell
            self.approximation[row][col] = updatedValue
        return np.copy(self.approximation)

    def solve(self):
        '''
        solve laplaces equation over the grid
        uses gauss-siedel iteration
        iterates until suitable maximum error
        '''
        errorThreshold = 0.001 
        current = self.timeStep()
        errorMatrix = np.zeros_like(self.approximation)
        maxError = 1

        while (abs(maxError) > errorThreshold):
            previous = current
            current = self.timeStep()
            updateErrorMatrix(previous, current, errorMatrix)
            maxError = np.amax(errorMatrix)
               
        #imshow solution
        im = plt.imshow(self.approximation, cmap='hot')
        plt.colorbar(im, orientation='vertical')
        plt.show()
    def choosePath(self):
        '''
        chooses direction where gradient is steepest
        only moves to directly adjacent cells
        '''
        neighbors = self.currentState.getNeighbors(self.currentPos)
        maxNeighbor = self.currentPos
        maxDifference = 0
        currentRow, currentCol = self.currentPos

        for neighbor in neighbors:
            row, col = neighbor
            difference = self.approximation[currentRow][currentCol] - self.approximation[row][col]

            if maxDifference < difference:
                maxNeighbor = neighbor
                maxDifference = difference
                
        return maxNeighbor 

        
def findMaxInMatrix(matrix):
    rows, cols = matrix.shape
    maximum = float(-inf)
    for row in range(rows):
        for col in range(cols):
            maximum = max(maximum, matrix[row][col])
    return maximum

def updateErrorMatrix(previous, current, errorMatrix):
    rows, cols = errorMatrix.shape
    for row in range(rows):
        for col in range(cols):
            if (previous[row][col] == 0):
                errorMatrix[row][col] = 0
            else:
                difference = current[row][col] - previous[row][col]
                error = difference/previous[row][col]
                errorMatrix[row][col] = error

def useSymmetry(neighbors):
    '''
    makes the list even so averaging neighbors is easier
    '''
    if len(neighbors) == 1:
        neighbor = deepcopy(neighbors[0])
        neighbors.append(neighbor)
        return neighbors

    return neighbors

#very basic, just to verify changes
#remove later

def test():
    s = LaplaceSolver(environments.testGridB)
    s.currentState.display()
    s.findOrdering()
    s.solve()
    print s.approximation
    print s.choosePath()
    return s
        
