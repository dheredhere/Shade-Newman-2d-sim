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
every environment has an occupancy grid and dimensions
Also needs methods to update the occupancy grid
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

    def getNeighbors(self, position):
        '''
    finds all valid neighbors from a cell
    returns a list
    '''
        row, col = position
        neighborPositions = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]

        #check for out-of-bounds errors and occupied space
        for position in neighborPositions[:]:
            if self.outOfBounds(position) or self.isOccupied(position):
                neighborPositions.remove(position)
        return neighborPositions

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
