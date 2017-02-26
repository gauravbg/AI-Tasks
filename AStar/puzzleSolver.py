import sys
import heapq
import time
'''
Created on Sep 28, 2016s

@author: Gaurav BG
'''


PROBLEM_SIZE = 9
RBFS_ExploredStates = 0
MAX_SEEN_IN_FRONTIER = 0

# Count of no of misplaced tiles in the puzzle
def heuristic1(state):
    
    counter = 1
    misplaced = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != counter and state[i][j] != PROBLEM_SIZE:
                misplaced = misplaced + 1
            counter = counter + 1

    return misplaced

# Classic Manhattan distance
def heuristic2(state):
    
    max = 4
    distance = 0
    if PROBLEM_SIZE == 9:
        max = 3
    for i in range(len(state)):
        for j in range(len(state[i])):
            number = state[i][j]
            if number != PROBLEM_SIZE:
                row = int((number-1) / max)
                col = (number-1) % max
                distance = distance + abs(row - i) + abs(col - j)

    return distance

#This returns true or false depending on the state passed is goal state or not
def goalTest(state):
    
    counter = 1
    correctTileCount = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == counter:
                correctTileCount = correctTileCount + 1
            counter = counter + 1    
    
    if correctTileCount == PROBLEM_SIZE:
        return True
    else: 
        return False  

#Decorated print for state
# This method is taken from the internet and is not part of submission. This is only used to view the states for debugging purposes. This method is not currently used in this code. 
def printState(state):
    s = [[str(e) for e in row] for row in state]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '  '.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


#Impln of RBFS algorithm
def RBFS(curNode, limit):
    #print("Currently Working on...")
    #printState(curNode.state)
            
    if goalTest(curNode.state):
        print("Found Solution with Cost =", curNode.g)
        #print("Total Explored States =", exploredStates)
        printPath(curNode.path)
        return [1, sys.maxsize]
    
    openNodes = []
    for action in range(4):
        genState = None
        if action == 0 and curNode.prevAction != 1:
            genState = generateState(curNode.state, action)
        elif action == 1 and curNode.prevAction != 0:
            genState = generateState(curNode.state, action)
        elif action == 2 and curNode.prevAction != 3:
            genState = generateState(curNode.state, action)
        elif action == 3 and curNode.prevAction != 2:
            genState = generateState(curNode.state, action)
        if genState != None:
            path = curNode.path[:]
            path.append(action)
            genNode = Node(genState, curNode.g+1, heuristic2(genState), action, path)
            heapq.heappush(openNodes, genNode)
    if len(openNodes) == 0:
        return [0, sys.maxsize]
    while True:
        best = heapq.heappop(openNodes)
        if best.f > limit:
            return [0, best.f]
        secondValue = sys.maxsize
        if len(openNodes) != 0:
            secondValue = openNodes[0].f
        result, best.f = RBFS(best, min(limit, secondValue))
        heapq.heappush(openNodes, best)
        if result == 1:
            return [result, sys.maxsize]
        
    
    
# This method will generate states from a given state and an action
# UP - 0, DOWN - 1, LEFT - 2, RIGHT - 3
def generateState(prevState, action):
    state = [x[:] for x in prevState]
    errorStatus = -1
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == PROBLEM_SIZE:
                if action == 0 and i != 0:
                    state[i][j] = state[i-1][j]
                    state[i-1][j] = PROBLEM_SIZE
                    errorStatus = 0
                elif action == 1 and i != len(state)-1:
                    state[i][j] = state[i+1][j]
                    state[i+1][j] = PROBLEM_SIZE
                    errorStatus = 0
                elif action == 2 and j != 0:
                    state[i][j] = state[i][j-1]
                    state[i][j-1] = PROBLEM_SIZE
                    errorStatus = 0
                elif action == 3 and j != len(state)-1:
                    state[i][j] = state[i][j+1]
                    state[i][j+1] = PROBLEM_SIZE
                    errorStatus = 0
            
            if errorStatus != -1:
                break
            
        if errorStatus != -1:
                break    
    
    if errorStatus == -1:
        return None
    else:
        return state
    
def printPath(path):
    pointer = 0
    for step in path:
        if step == 0:
            print("U", end = ",")
            out_file.write('U')
        elif step == 1:
            print("D", end = ",")
            out_file.write('D')
        elif step == 2:
            print("L", end = ",")
            out_file.write('L')
        elif step == 3:
            print("R", end = ",")
            out_file.write('R')
        if pointer != len(path)-1:
            out_file.write(',')
            pointer = pointer + 1
    print("G")
    
        

#This class represents node which holds state, heuristic value, g value and f value, path and previous action
class Node:
    def __init__(self, st, g, h, prev, pth):
        self.state = st
        self.g = g
        self.h = h
        self.prevAction = prev #Tree search requirement
        self.f = self.h + self.g
        self.path = pth
    
    def __cmp__(self, other):
        return cmp(self.f, other.f)
    
    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.f== other.f

   

if __name__ == '__main__':

    
    frontier = []
    algoNumber = 0
    k = -1
    out_file = ''
    in_file = ''
    state = []
    exploredStates = 0
    start_time = time.clock()
    
    if len(sys.argv) == 5:
        algoNumber = int(sys.argv[1])
        k = int(sys.argv[2])
        in_file = open(sys.argv[3], 'r')
        out_file = open(sys.argv[4], 'w')
    else:
        print('Wrong number of arguments', len(sys.argv))
    global PROBLEM_SIZE
    global MAX_SEEN_IN_FRONTIER
    if k == 3:
        PROBLEM_SIZE = 9
    elif k == 4:
        PROBLEM_SIZE = 16
        
        
    content = in_file.read().splitlines()

    counter = 0
    x = 0
    y = 0
    for line in content:
        state.append([])
        for n in line.split(','):
            if(n == ''):
                n = PROBLEM_SIZE
            state[counter].append(int(n)) 
        counter = counter + 1
    
    print("Original Problem State: ")
    printState(state)
    emptyPath = []
    firstNode = Node(state, 0, heuristic2(state), -1, emptyPath)
    
    
    if int(algoNumber) == 1: # A* Algorithm
        print("Solving using A* Algorithm: ")
        heapq.heappush(frontier, firstNode)
        while len(frontier) != 0:
            curNode = heapq.heappop(frontier)
            exploredStates = exploredStates + 1
            #print("Currently Working on...")
            #printState(curNode.state)
            
            if curNode.h == 0:
                print("Found Solution with Cost =", curNode.g)
                print("Total Explored States =", exploredStates)
                printPath(curNode.path)
                break
            
            for action in range(4):
                genState = None
                if action == 0 and curNode.prevAction != 1:
                    genState = generateState(curNode.state, action)
                elif action == 1 and curNode.prevAction != 0:
                    genState = generateState(curNode.state, action)
                elif action == 2 and curNode.prevAction != 3:
                    genState = generateState(curNode.state, action)
                elif action == 3 and curNode.prevAction != 2:
                    genState = generateState(curNode.state, action)
                if genState != None:
                    path = curNode.path[:]
                    path.append(action)
                    genNode = Node(genState, curNode.g+1, heuristic2(genState), action, path)
                    heapq.heappush(frontier, genNode)
            if len(frontier) > MAX_SEEN_IN_FRONTIER:
                MAX_SEEN_IN_FRONTIER = len(frontier)
                
    elif int(algoNumber) == 2: # RBFS Algorithm
        print("Solving using RBFS Algorithm: ")
        solutionState = RBFS(firstNode, sys.maxsize)
        
    end_time = time.clock()
    print("Total Program execution time in milliseconds = " + str((end_time - start_time)*100))
    #print("MAX_SEEN_IN_FRONTIER = " ,MAX_SEEN_IN_FRONTIER)
    
        
    
    

    
    
    
    
    
    
       
    
