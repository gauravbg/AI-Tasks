import sys
import time
import copy
'''
Created on Oct 30, 2016

@author: Gaurav BG
'''
maxCount = 0
arcPruningCount = 0

# Pruning function of the AC-3 Algorithm
def pruneDomain(arc, domain):
    global arcPruningCount
    arcPruningCount = arcPruningCount + 1
    changed = 0
    for i in domain[arc[0]]:
        foundConsistency = False
        for j in domain[arc[1]]:
            if i != j:
                foundConsistency = True
                break
        if foundConsistency == False:
            domain[arc[0]].remove(i) 
            changed = changed + 1
    if len(domain[arc[0]]) == 0:
        return 1, changed
    else:
        return 0, changed

# AC-3 Algorithm
def makeDomainArcConsistent(neighbourMap, domain):
    arcsList = []
    for x in neighbourMap:
        for y in neighbourMap[x]:
            arcsList.append([x, y])
    while len(arcsList) != 0:
        arc = arcsList.pop(0)
        abort, changed = pruneDomain(arc, domain)
        if abort == 1:
            return abort
        if changed != 0:
            for neighbour in neighbourMap[arc[0]]:
                if [neighbour, arc[0]] not in arcsList:
                    arcsList.append([neighbour, arc[0]])
    return 0

# Returns a list with conflicting variables for the current assignment (Used here to verify the final answer)
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



# Choosing value that least constraints others
def getBestAssignment(variable, neighbourMap, domain, alreadySelected):
    
    leastPruned = n
    remSet = set(domain[variable]) - set(alreadySelected)
    remList = list(remSet)
    bestAssignment = remList[0]
        
    for value in remList:
        totalPruned = 0
        for neighbor in neighbourMap.get(variable):
            if value in domain[neighbor]:
                totalPruned = totalPruned + 1
        if totalPruned < leastPruned: 
            leastPruned = totalPruned
            bestAssignment = value
    return bestAssignment      

# Simple DFS algorithm with backtracking
def DFSB(variable, neighbourMap, assignment, count):
    intermediate_time = time.clock()
    if (intermediate_time - start_time) > 60:
        return 0
    global maxCount
    if count > maxCount:
        maxCount = count
    if count >= n:
        print("Answer = ", assignment)
        for decision in assignment:
            out_file.write(str(decision))
            out_file.write('\n')
        somelist = getConflictingVariables(neighbourMap, assignment)
        if len(somelist) == 0:
            print("Assignment is Verified for correctness")
        else:
            print("Conflicts found in ", len(somelist))
        return 1
    for var in range(k):
        conflictFound = False
        for neighbour in neighbourMap.get(variable):
            if assignment[neighbour] == var:
                conflictFound = True
                break
          
        if conflictFound == False:
            assignment[variable] = var
            result = DFSB((variable+1), neighbourMap, assignment, (count+1))
            if result == 0:
                assignment[variable] = -1
            else:
                return 1
    return 0    
    

# DFS algorithm with backtracking, MRV, least constraint value, forward checking and AC-3 Pruning
def DFSB_plus(variable, domain, neighbourMap, assignment, count):
    global maxCount
    if count > maxCount:
#         print("count= " , count)
        maxCount = count
    if count >= n:
        print("Answer = ", assignment)
        for decision in assignment:
            out_file.write(str(decision))
            out_file.write('\n')
        print("Arc pruning calls count = " , arcPruningCount)
        somelist = getConflictingVariables(neighbourMap, assignment)
        if len(somelist) == 0:
            print("Assignment is Verified for correctness")
        else:
            print("Conflicts found in ", len(somelist))
        return 1
    if len(domain[variable]) == 0:
        return 0
        
    
    alreadySelected = []
    counter = 0
    
    
    while counter < len(domain[variable]):
        oldDomain = copy.deepcopy(domain)
        bestAssignment = getBestAssignment(variable, neighbourMap, domain, alreadySelected)
        alreadySelected.append(bestAssignment)
        assignment[variable] = bestAssignment
        
        abort = 0
        domain[variable] = [bestAssignment]
    
        
        # Forward checking idea implemented below
        for neighbor in neighbourMap.get(variable):
            if bestAssignment in domain[neighbor]:
                domain[neighbor].remove(bestAssignment)
            if len(domain[neighbor]) == 0:
                abort = 1
                break
        if abort == 1:
            counter = counter + 1
            assignment[variable] = -1
            domain = oldDomain
            continue
        
        
        # Arc consistency checked below
        abort = makeDomainArcConsistent(neighbourMap, domain)
        
        if abort == 1:           
            counter = counter + 1
            assignment[variable] = -1
            domain = oldDomain
            continue
        
        # Minimum remaining variable implemented below        
        least = k
        MRV = 0
        for j in range(len(domain)):
            if assignment[j] == -1:
                MRV = j
                least = len(domain[j])
                break
        for j in range(len(domain)):
            if assignment[j] != -1:
                continue
            if len(domain[j]) < least:
                MRV = j 
                least = len(domain[j])
        
        result = DFSB_plus(MRV, domain, neighbourMap, assignment, (count+1))
        if result == 0:
            assignment[variable] = -1
            domain = oldDomain 
        else:
            return 1
        counter = counter + 1
        domain = oldDomain
    
    
    return 0

if __name__ == '__main__':

    
    algoType = 0
    out_file = ''
    in_file = ''
    n = 0
    m = 0
    k = 0
    neighbourMap = {}
    domain = []
    assignment = []
    global arcPruningCount
    start_time = time.clock()
    
    if len(sys.argv) == 4:
        in_file = open(sys.argv[1], 'r')
        out_file = open(sys.argv[2], 'w')
        algoType = int(sys.argv[3])
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
        
    if algoType == 0:
        result = DFSB(0, neighbourMap, assignment, 0)
    else:    
        result = DFSB_plus(0, domain, neighbourMap, assignment, 0)
    end_time = time.clock()
    if result == 0:
        print("No result found in " + str((end_time - start_time)) + " seconds")
    else:
        print("Total Program execution time in seconds = " + str((end_time - start_time)))
    

            

    