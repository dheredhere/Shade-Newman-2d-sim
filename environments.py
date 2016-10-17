import numpy as np

'''
utils to easily create and display 2d environments 
converts array of strings to 2d numpy array and vice versa

Free space: stored as 1, displayed as O
Occupied space: stored as -1, displayed as X
Unexplored space: stored as 0, displayed as ?
'''

charToCell = {
        'O': 1,    
        'X': -1,  
        '?': 0, }

#temporary, only for debugging
cellToChar = {
        -1: 'X',
        0: '?',
        1: 'O' }

def stringsToMatrix(stringArray): 
    rows = len(stringArray)
    cols = len(stringArray[0])
    grid = np.zeros(shape=(rows, cols))

    for row in range(rows):
        if len(stringArray[row]) != cols:
            print("Error!\nThis row has an incorrect number of characters:\n")
            print row

        for col in range(cols):
            char = stringArray[row][col]
            grid[row][col] = charToCell[char]

    return grid

'''
Environment class
Has occupancy grid, dimensions, methods to update,
methods to get neighboring cells (x and y direction)
'''

class Environment:
    def __init__(self,stringArray):
        self.grid = stringsToMatrix(stringArray)
        self.rows, self.cols = self.grid.shape
        self.dimensions = (self.rows, self.cols)

    def getDimensions(self):
        return self.dimensions

    def display(self):
        displayString = ''
        for row in self.grid:
            rowString = ''
            for cell in row:
                rowString += cellToChar[cell]
            displayString += rowString + '\n'
        print displayString
        return displayString

    def isOccupied(self, position):
        row, col = position
        return self.grid[row][col] == -1

    def isUnexplored(self, position):
        row, col = position
        return self.grid[row][col] == 0

    '''
    WARNING!
    All the following getNeighbor functions DONT return unexplored space
    they are filtered by filterNeighbors which ensures this
    might have to add more in the future
    '''
    def getRowNeighbors(self, position):
        '''
        returns list of free space neighbors in row
        '''
        row, col = position
        rowNeighbors = [(row, col+1), (row, col-1)]
        return self.filterFreeNeighbors(rowNeighbors)

    def getColNeighbors(self, position):
        '''
        returns list of free space neighbors in column
        '''
        row, col = position
        colNeighbors = [(row+1, col), (row-1, col)]
        return self.filterFreeNeighbors(colNeighbors)

    def getNeighbors(self, position):
        '''
        returns list of all valid neighbors
        (one manhattan distance away)
        IMPORTANT: filters out unexplored neighbors
        '''
        neighbors = self.getColNeighbors(position) + self.getRowNeighbors(position)
        return self.filterExploredNeighbors(neighbors)

    def filterExploredNeighbors(self, neighbors):
        '''
        removes invalid neighbors in list
        IMPORTANT: also removes unexplored neighbors
        '''
        for neighbor in neighbors[:]:
            if self.outOfBounds(neighbor) or self.isOccupied(neighbor) or self.isUnexplored(neighbor):
                neighbors.remove(neighbor)
        return neighbors

    def filterFreeNeighbors(self, neighbors):
        '''
        removes invalid neighbors in list
        keeps unexplored neighbors, removes occupied neighbors
        '''
        for neighbor in neighbors[:]:
            if self.outOfBounds(neighbor) or self.isOccupied(neighbor):
                neighbors.remove(neighbor)
        return neighbors

    def outOfBounds(self, coordinate):
        rows, cols = self.getDimensions()
        return coordinate[0] < 0 or coordinate[1] < 0 or coordinate[0] >= rows or coordinate[1] >= cols


'''
simple environment instances for testing
XXX
XO?
XXX
'''

testGridA = Environment(["XXX", "XO?", "XXX"])

'''
XXXX
XOO?
XOO?
XXXX
'''

testGridB = Environment(["XXXX", "XOO?", "XOO?", "XXXX"])

