import sys
import time
import random
'''
Created on Oct 31, 2016

@author: Gaurav BG
'''

# Gets a random assignment for each variable
def getRandomAssignment(assignment):
    for i in range(len(assignment)):
        assignment[i] = random.randint(0, k-1)
    return

# Returns a list with conflicting variables for the current assignment
def getConflictingVariables(neighbourMap, assignment):
    
    conflictingVariables =[]
    for i in range(len(assignment)):
        conflicts = False
        for neighbour in neighbourMap[i]:
            if assignment[neighbour] == assignment[i]:
                conflicts = True
        if conflicts == True:
            conflictingVariables.append(i)
    return conflictingVariables

# Returns next variable and assignment value which reduces the total no of conflicts
def pickNextVariableAndAssignment(listWithConflicts, neighbourMap, assignment):
    
    minConflicts = n
    bestAssignment = 0

    bestVariable = random.choice(listWithConflicts)
    for i in range(k):
        conflicts = 0
        if i != assignment[bestVariable]:
            for neighbour in neighbourMap[bestVariable]:
                if assignment[neighbour] == i:
                    conflicts = conflicts + 1
            if conflicts < minConflicts:
                minConflicts = conflicts
                bestAssignment = i
    return bestVariable, bestAssignment

# Implementation of Min-Conflicts algorithm
def minConflicts(neighbourMap, assignment, iterations):
    
    while iterations >= 0:
        intermediate_time = time.clock()
        if (intermediate_time - start_time) > 60:
            return -1
        listWithConflicts = getConflictingVariables(neighbourMap, assignment)
        if len(listWithConflicts) == 0:
            print("Answer = ", assignment)
            print("Search Steps = ", (10000-iterations))
            for decision in assignment:
                out_file.write(str(decision))
                out_file.write('\n')
            return 1
        nextVariable, nextAssignmentValue = pickNextVariableAndAssignment(listWithConflicts, neighbourMap, assignment)
        assignment[nextVariable] = nextAssignmentValue
        iterations = iterations - 1
    print("Ran out of iterations")
    return 0   

if __name__ == '__main__':

    
    out_file = ''
    in_file = ''
    n = 0
    m = 0
    k = 0
    neighbourMap = {}
    domain = []
    assignment = []
    start_time = time.clock()
    
    if len(sys.argv) == 3:
        in_file = open(sys.argv[1], 'r')
        out_file = open(sys.argv[2], 'w')
    else:
        print('Wrong number of arguments', len(sys.argv))
    content = in_file.read().splitlines()
    firstLine = content[0].split()
    n = int(firstLine[0])
    m = int(firstLine[1])
    k = int(firstLine[2])
    for line in range(1, len(content)):
        con = content[line].split()
        constraint = []
        constraint.append(int(con[0]))
        constraint.append(int(con[1]))
        if constraint[0] not in neighbourMap:
            neighbourMap[constraint[0]] = []
        neigbours = neighbourMap.get(constraint[0])
        if constraint[1] not in neigbours:
            neigbours.append(constraint[1])
        neighbourMap[constraint[0]] = neigbours
        if constraint[1] not in neighbourMap:
            neighbourMap[constraint[1]] = []
        neigbours = neighbourMap.get(constraint[1])
        if constraint[0] not in neigbours:
            neigbours.append(constraint[0])
        neighbourMap[constraint[1]] = neigbours
    print("Neighbour Graph:")
    for x in neighbourMap:
        print(x, ":", neighbourMap[x])
    for i in range(n):
        domain.append(list(range(0, k)))
        assignment.append(-1)
    result = 0
    while result == 0:
        getRandomAssignment(assignment)
        result = minConflicts(neighbourMap, assignment, 10000)
    end_time = time.clock()
    if result == -1:
        print("No result found in " + str((end_time - start_time)) + " seconds")
    else:
        print("Total Program execution time in seconds = " + str((end_time - start_time)))
    
