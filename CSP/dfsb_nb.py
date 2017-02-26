# Artificial Intelligence Assignment 2
# Student Name: Nipun Bayas
# ID: 110944898

# python dfsb.py <INPUT_FILE_PATH> <OUTPUT_FILE_PATH> <mode_flag>
# where,
# INPUT_FILE_PATH = The path to the input file.
# OUTPUT_FILE_PATH = The path to the output file
#  mode_flag: 0 = DFS-B and 1 = DFS-B++

import sys
import copy
from datetime import datetime


def write_solution(solution):
    output = open(output_file, 'w')
    if solution is not None:
        for item in solution.values():
            output.write("%s\n" % item)
    else:
        output.write("No answer")
    output.close()


def dfsb(assigned, no_of_calls):
    if ((datetime.now() - start_time).total_seconds()) >= 60:
        return None

    if len(assigned) == no_of_variables:
        end_time = datetime.now()
        print((end_time - start_time).microseconds / 1000)
        return assigned

    no_of_calls += 1

    for var in variables:
        if var not in assigned:
            unassigned_variable = var
            break

    for color in domains:
        count = 0
        for neighbour in constraints[unassigned_variable]:
            if assigned.get(neighbour) == color:
                count += 1
        if count == 0:
            assigned[unassigned_variable] = color
            recursive_backtracking = dfsb(assigned, no_of_calls)
            if recursive_backtracking is not None:
                return recursive_backtracking
        if assigned.get(unassigned_variable):
            del assigned[unassigned_variable]
    return None


def dfsb_enhanced(unassigned_variable, assigned, no_of_calls, possible_domains):
    start_time = datetime.now()
    queue = []

    if ((datetime.now() - start_time).total_seconds()) >= 60:
        return 0

    length_var_constraints = 100000

    if len(assigned) == no_of_variables:
        end_time = datetime.now()
        print((end_time - start_time).microseconds / 1000)
        print("Solution is: ", assigned)
        write_solution(assigned)
        return 1

    if len(possible_domains[unassigned_variable]) == 0:
        print("Returned from: ", unassigned_variable)
        return 0

    # LCV
    possible_domains[unassigned_variable] = least_constrained_value(unassigned_variable)

    for clr in possible_domains[unassigned_variable]:
        old_possible_domain = copy.deepcopy(possible_domains)
        assigned[unassigned_variable] = clr
        possible_domains[unassigned_variable] = [clr]

    # Forward Checking
        for neighbour in constraints[unassigned_variable]:
            if clr in possible_domains[neighbour]:
                possible_domains[neighbour].remove(clr)

      # AC 3 implementation
        for var in variables:
            for neighbour in constraints[var]:
                queue.append((var, neighbour))

        while queue:
            no_of_calls += 1
            print(no_of_calls)
            (var, neighbour) = queue.pop(0)
            if remove_inconsistent_values(var, neighbour):
                for neighbour in constraints[var]:
                    if (neighbour, var) not in queue:
                        queue.append((neighbour, var))

        # MRV
        next_unassigned_variable = 0
        for var in variables:
            if var not in assigned:
                next_unassigned_variable = var
                break
        for var in variables:
            if (len(possible_domains[var]) <= length_var_constraints) and var not in assigned:
                length_var_constraints = len(possible_domains[var])
                next_unassigned_variable = var

        result = dfsb_enhanced(next_unassigned_variable, assigned, no_of_calls, possible_domains)
        if result == 0:
            possible_domains = old_possible_domain
            #print("size = ", possible_domains[unassigned_variable], color)
            del assigned[unassigned_variable]
        else:
            return 1
        possible_domains = old_possible_domain
    return 0


def least_constrained_value(variable):
    conflicts = dict()
    colors = []
    for color in possible_domains[variable]:
        count = 0
        for neighbour in constraints[variable]:
            if color in possible_domains.get(neighbour, None):
                count += 1
        conflicts[color] = count
    for w in sorted(conflicts, key=conflicts.get):
        colors.append(w)
    return colors


def remove_inconsistent_values(var, neighbour):
    popped = False
    for variable_color in possible_domains[var]:
        count = 0
        for neighbour_color in possible_domains[neighbour]:
            if variable_color != neighbour_color:
                count += 1
        if count == 0:
            possible_domains[var].remove(variable_color)
            popped = True
    return popped


def find_conflicted_var():
    conflicting_vars = []
    for variable in variables:
        count = 0
        for neighbour in constraints[variable]:
            if assigned.get(neighbour, None) == assigned.get(variable, None):
                count += 1
        if count > 0:
            conflicting_vars.append(variable)

    return conflicting_vars


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("ERROR: Invalid number of arguments. \nUSAGE: dfsb.py <INPUT_FILE_PATH> <OUTPUT_FILE_PATH> <mode_flag>")
        sys.exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    assigned = dict()
    variables = []
    domains = []
    constraints = dict()
    solution = dict()
    no_of_calls = 0

    with open(input_file) as inputted_file:
        lines = inputted_file.read().splitlines()   # read input file

    output = open(output_file, 'w')

    # determine the number of variables, constraints and possible colors
    no_of_variables = int(lines[0].split()[0])
    no_of_constraints = int(lines[0].split()[1])
    possible_colors = int(lines[0].split()[2])

    for i in range(int(lines[0].split()[0])):
        variables.append(i)

    for i in range(int(lines[0].split()[2])):
        domains.append(i)

    for i in range(1, len(lines), 1):
        line = lines[i]
        if int(line.split()[0]) in constraints:
            constraints[int(line.split()[0])].append(int(line.split()[1]))
            if int(line.split()[1]) in constraints:
                constraints[int(line.split()[1])].append(int(line.split()[0]))
            else:
                constraints[int(line.split()[1])] = [int(line.split()[0])]
        else:
            constraints[int(line.split()[0])] = [int(line.split()[1])]
            if int(line.split()[1]) in constraints:
                constraints[int(line.split()[1])].append(int(line.split()[0]))
            else:
                constraints[int(line.split()[1])] = [int(line.split()[0])]

    for i in range(int(lines[0].split()[0])):
        if i not in constraints:
            constraints[i] = []

    print("Variables are:", variables)
    print("Domains are: ", domains)
    print("Constraints are: ", constraints)

    if int(sys.argv[3]) == 0:
        print("Called DFS-B")
        start_time = datetime.now()
        solution = dfsb(assigned, no_of_calls)
        print("Solution is: ", solution)
        write_solution(solution)

    elif int(sys.argv[3]) == 1:
        print("Called DFS-B with MRV, LCV + AC3")

        possible_domains = dict()
        old_possible_domain = dict()

        for variable in variables:
            for color in domains:
                if variable in possible_domains:
                    possible_domains[variable].append(color)
                else:
                    possible_domains[variable] = [color]

        old_possible_domain = copy.deepcopy(possible_domains)

        solution = dfsb_enhanced(0, assigned, no_of_calls, possible_domains)
        print("Solution is: ", solution)
        conf_vars = find_conflicted_var()
        print("Conflicted vars are: ", conf_vars)

        if solution is 0:
            output.write("No answer")
            output.close()

    else:
        print("Incorrect <mode_flag> selected. Please choose 0 or 1")