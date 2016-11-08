import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import random
from math import log, exp

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

#only for debugging
cellToChar = {
        -1: 'X',
        0: '?',
        1: 'O' }

#use 10 as the location for the drone?
cmap = mpl.colors.ListedColormap(['black', 'purple', 'white', 'green'])
bounds = [-2, -.0001, .0001, 2, 12]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

def stringsToMatrix(stringArray): 
    rows = len(stringArray)
    cols = len(stringArray[0])
    currentState = np.zeros(shape=(rows, cols))

    for row in range(rows):
        if len(stringArray[row]) != cols:
            print("Error!\nThis row has an incorrect number of characters:\n")
            print row

        for col in range(cols):
            char = stringArray[row][col]
            currentState[row][col] = charToCell[char]

    return currentState

#some utils for logodds stuff

def logit(p):
    return log(p/(1-p))

def inverseLogit(a):
    b = exp(a)
    return b/(1+b)

'''
Environment class
Has occupancy currentState, dimensions, methods to update,
methods to get neighboring cells (x and y direction)
'''

class Environment:
    def __init__(self, exploredStringArray, startPos, initStringArray=None):
        self.goalState = stringsToMatrix(exploredStringArray)
        self.logodds = np.zeros_like(self.goalState)
        self.rows, self.cols = self.goalState.shape
        self.currentPos = startPos
        self.errorProbability = .1
        
        if (initStringArray == None):
            #set self.current state = to a grid of unexplored cells
            #call self.move() to find adjacent cells from start location
            self.currentState = np.zeros_like(self.goalState)

            #take x sensor scans at initialization
            for x in range(5):
                self.move(startPos)
            
        else :
            self.currentState = stringsToMatrix(initStringArray)

        self.dimensions = (self.rows, self.cols)

    def getDimensions(self):
        return self.dimensions

    def display(self):
        displayString = ''
        for row in self.currentState:
            rowString = ''
            for cell in row:
                rowString += cellToChar[cell]
            displayString += rowString + '\n'
        #print displayString

        x, y = self.currentPos
        value = self.currentState[x][y]
        self.currentState[x][y] = 10

        img = plt.imshow(self.currentState, interpolation='nearest', cmap = cmap, norm=norm)
        plt.colorbar(img, cmap=cmap, norm=norm, boundaries = bounds, ticks=[-1,0,1])
        plt.show()

        self.currentState[x][y] = value
        return displayString

    def isOccupied(self, position):
        row, col = position
        return self.currentState[row][col] < 0

    def isUnexplored(self, position):
        row, col = position
        return self.currentState[row][col] == 0

    def move(self, newPos):
        '''
        need to update values in a radius
        mxn is dimensions of the environment
        '''
        self.currentPos = newPos
        a, b = newPos
        m, n = self.rows, self.cols
        r = 2
        y, x = np.ogrid[-a:m-a, -b:n-b]

        mask = x*x + y+y <= r*r

        #self.currentState[mask] = self.goalState[mask]
        #updatedCells = np.zeros_like(self.currentState)

        for row in range(0, self.rows):
            for col in range (0, self.cols):
                if mask[row][col] == True:
                    print (row, col)
                    
                    sensorVal = self.detectCell((row, col))

                    if (sensorVal == 1): #cell is free
                        #there is a p chance of it being occupied (p is error)
                        self.logodds[row][col] += logit(self.errorProbability)
                    elif (sensorVal == -1): #cell is occupied
                        #there is a 1-p chance of it being occupied 
                        self.logodds[row][col] += logit(1-self.errorProbability)
                        
                    #now update any cells whose probabilities may have changed
                    #TODO add thresholds in the future, ie if .4 <= p <= .6, undetermined
                    #if p(occupied) > .5, then cell is occuped
                    if self.logodds[row][col] > 0:
                        self.currentState[row][col] = -1

                    #if p(occupied) < .5, then cell is empty
                    elif self.logodds[row][col] <= 0:
                        self.currentState[row][col] = 1
        #self.display() 

    def detectCell(self, coordinate):
        '''
        returns cell with random chance of error
        '''
        row, col = coordinate
        val = self.goalState[row][col]
        if (random.random() <= self.errorProbability): #return error with probability p
            print "sensor error!"
            val = val * -1
        return val

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
        IarrayMarrayPORTANT: filters out unexplored neighbors
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
XXXX??
XOOX??
XOO???
XXXX??

XXXXXX
XOOXOX
XOOOOX
XXXXXX
'''

testGridA = Environment(["XXXXXX", "XOOXOX", "XOOOOX", "XXXXXX"], (1, 1), ["XXXX??", "XOOX??", "XOO???", "XXXX??"])

testGridB = Environment(["XXXXXX", "XOOXOX", "XOOOOX", "XXXXXX"], (1, 1))

