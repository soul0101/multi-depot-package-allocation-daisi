import math
from ortools.linear_solver import pywraplp
from sklearn.metrics import pairwise

def initialize_cost(depot_locations, drop_locations):
    """
    Initializes the cost matrix
    """
    cost = pairwise.haversine_distances([[math.radians(_[0]), math.radians(_[1])] for _ in depot_locations] , [[math.radians(_[0]), math.radians(_[1])] for _ in drop_locations] ) * 6371
    return cost

def initialize_solver(costs, depot_capacities, num_depots, num_drops):

    """
    - Create the mip solver with the CBC backend.
    - Set to GUROBI for faster and more optimized results (Requires license)
    """

    solver = pywraplp.Solver.CreateSolver('CBC')

    """
    Variables
    ----------
    allocation_matrix[i, j] is an array of 0-1 variables, which will be 1
    if depot i is assigned to drop j.
    """

    allocation_matrix = {}
    for depot in range(num_depots):
        for drop in range(num_drops):
            allocation_matrix[depot, drop] = solver.BoolVar(f'x[{depot},{drop}]')
    
    """
    Constraints
    ------------
    - The total size of the drops each depot i takes on is at most depot_capacities[i]
    - Each drop is assigned to exactly one or none depot.
    """
    for depot in range(num_depots):
        solver.Add(
            solver.Sum([
                allocation_matrix[depot, drop] for drop in range(num_drops)
            ]) <= depot_capacities[depot])

    for drop in range(num_drops):
        solver.Add(
            solver.Sum([allocation_matrix[depot, drop] for depot in range(num_depots)]) <= 1)

    """
    Objective
    """
    objective_terms = []
    for depot in range(num_depots):
        for drop in range(num_drops):
            objective_terms.append(costs[depot][drop] * allocation_matrix[depot, drop])
    
    for drop in range(num_drops):
        objective_terms.append(500 * (1 - solver.Sum([allocation_matrix[depot, drop] for depot in range(num_depots)])))

    solver.set_time_limit(10*1000)
    solver.Minimize(solver.Sum(objective_terms))

    """
    Solver
    """
    status = solver.Solve()
    return allocation_matrix, status, solver

def optimize(depot_locations, drop_locations, depot_capacities):
    num_depots = len(depot_locations)
    num_drops = len(drop_locations)

    costs = initialize_cost(depot_locations, drop_locations)
    allocation_matrix, status, solver = initialize_solver(costs, depot_capacities, num_depots, num_drops)

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {solver.Objective().Value()}\n')

        allocations={}

        for depot in range(num_depots):
            for drop in range(num_drops):
                if allocation_matrix[depot, drop].solution_value() > 0.5: 
                    if depot in allocations:
                        allocations[depot].append(drop)
                    else:
                        allocations[depot] = []
                        allocations[depot].append(drop)

        return allocations
    else:
        print('No solution found.')
