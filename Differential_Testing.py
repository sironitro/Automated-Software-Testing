import os
import random
import sys
import cplex
import gurobipy as grb
from docplex.mp.model import Model
import time

arithmetic_operators = ['+', '-', '*', '/']
relational_operators = ['E', 'L', 'G'] # constraints relational operators
MAX_INT_32 = 2147483647


def cplex_model(objective, lower_bounds, upper_bounds, names, constraints, constraint_senses, rhs, constraint_names, obj_max):
    cplex_model = cplex.Cplex()
    if obj_max:
        cplex_model.objective.set_sense(cplex_model.objective.sense.maximize)
    else:
        cplex_model.objective.set_sense(cplex_model.objective.sense.minimize)
    cplex_model.variables.add(obj = objective, lb = lower_bounds, ub = upper_bounds, names = names)
    cplex_model.linear_constraints.add(lin_expr = constraints, senses = constraint_senses, rhs = rhs, names = constraint_names)
    s = cplex_model.solve()
    try:
        cplex_obj = cplex_model.solution.get_objective_value()
        cplex_vars = cplex_model.solution.get_values()
        return cplex_obj, cplex_vars
    except:
        return None, None

def grb_model(names, lower_bounds, upper_bounds, constraints, constraint_senses, rhs, objective, obj_max):
    grb_model = grb.Model()
    variables = []
    for name, lb, ub in zip(names, lower_bounds, upper_bounds):
        var = grb_model.addVar(name=name, lb=lb, ub=ub, vtype=grb.GRB.CONTINUOUS)
        variables.append(var)
    for i in range(len(constraints)):
        lhs = grb.LinExpr(constraints[i][1], variables)
        grb_model.addLConstr(lhs=lhs, sense=constraint_senses[i], rhs=rhs[i])
    if obj_max:
        grb_model.ModelSense = grb.GRB.MAXIMIZE
    else:
        grb_model.ModelSense = grb.GRB.MINIMIZE
    grb_model.setObjective(grb.LinExpr(objective, variables))
    grb_model.optimize()
    if grb_model.Status == grb.GRB.OPTIMAL or grb_model.Status == grb.GRB.SUBOPTIMAL:
        return grb_model.ObjVal, [v.X for v in grb_model.getVars()]
    else:
        return None, None

def print_output(type, obj, vals, names):
    print(type)
    if (obj is None):
        print("Model is infeasible")
        return
    print("Objective =", obj)
    for v, name in zip(vals, names):
        print(name, "=", v)

def is_identical(cplex_obj, grb_obj, cplex_vals, grb_vals, names):
    print_output("CPLEX", cplex_obj, cplex_vals, names)
    print_output("Gurobi", grb_obj, grb_vals, names)
    if cplex_obj is None and grb_obj is None and cplex_vals is None and grb_vals is None:
        return True
    elif cplex_obj == grb_obj and all([abs(cplex_val - grb_val) < 1e-6 for cplex_val, grb_val in zip(cplex_vals, grb_vals)]):
        return True
    else:
        print("Potential Bug Found: CPLEX and Gurobi models are not identical")
        print_output("CPLEX", cplex_obj, cplex_vals, names)
        print_output("Gurobi", grb_obj, grb_vals, names)
        return False

def get_mutation_operator():
    mutation_operators = ["model sense", "relational operator replacement", "abs", "unary operator insertion"]
    return random.choice(mutation_operators)

def random_val_replace():
    return random.choice(["constraint", "objective"])

def test_linear_prog(num_runs, filename):
    start_time = time.time()
    potential_bugs = 0
    mutations_performed = 0
    mutation_log = []

    #  define variables
    names = ['x', 'y']
    lower_bounds = [100, 100]
    upper_bounds = [cplex.infinity, cplex.infinity]

    # define constraints
    constraint_names = ["c1", "c2"]
    first_constraint = [[0,1], [0.2, 0.4]]
    second_constraint = [[0,1], [0.5, 0.4]]
    constraints = [first_constraint, second_constraint]
    rhs = [400, 490]
    constraint_senses = ['L', 'L']

    # define objective
    objective = [12, 20]
    obj_max = True

    for i in range(num_runs):
        mutation_operator = get_mutation_operator()
        print("Mutation Operator:", mutation_operator)
        if mutation_operator == "relational operator replacement":
            index = random.randint(0, len(constraint_senses)-1)
            old_value = constraint_senses[index]
            constraint_senses[index] = random.choice(relational_operators)
            print(index, constraint_senses[index])
            if (old_value != constraint_senses[index]):
                mutations_performed += 1
                mutation_log.append(f"Relational Operator changed from {old_value} to {constraint_senses[index]}")

        if mutation_operator == "model sense": 
            old_value = obj_max
            obj_max = random.choice([True, False])
            print("model sense", obj_max)
            if (old_value != obj_max):
                mutations_performed += 1
                if obj_max:
                    mutation_log.append(f"Model Sense changed from Minmizing to Maximizing")
                else:
                    mutation_log.append(f"Model Sense changed from Maximizing to Minimizing")
        
        if mutation_operator == "abs":
            index = random.randint(0, len(constraints)-1)
            index2 = random.randint(0, len(constraints[index][1])-1)
            old_value = constraints[index]
            constraints[index][1][index2] = abs(constraints[index][1][index2])
            if old_value != constraints[index]:
                mutations_performed += 1
                mutation_log.append(f"Absolute value inserted at index {index2} of constraint {index}")

        if mutation_operator == "unary operator insertion":
            if random_val_replace() == "constraint":
                index = random.randint(0, len(constraints)-1)
                index2 = random.randint(0, len(constraints[index][1])-1)
                old_value = constraints[index]
                constraints[index][1][index2] = -1 * + constraints[index][1][index2]
                print(constraints)
                if old_value != constraints[index]:
                    mutations_performed += 1
                    if constraints[index][1][index2] <= 0:
                        mutation_log.append(f"Unary operator inserted at index {index2} of constraint {index}")
                    else:
                        mutation_log.append(f"Unary operator removed at index {index2} of constraint {index}")
            elif random_val_replace() == "objective":
                index = random.randint(0, len(objective)-1)
                old_value = objective[index]
                objective[index] = -1 * + objective[index]
                print(objective)
                if old_value != objective[index]:
                    mutations_performed += 1
                    if objective[index] <= 0:
                        mutation_log.append(f"Unary operator inserted at index {index} of objective")
                    else:
                        mutation_log.append(f"Unary operator removed at index {index} of objective")

        # random scalar variable replacement
        if random_val_replace() == "constraint":
            index = random.randint(0, len(constraints)-1)
            old_value = constraints[index]
            index2 = random.randint(0, len(constraints[index][1])-1)
            constraints[index][1][index2] = random.randint(0, MAX_INT_32)
            print(constraints)
            if old_value != constraints[index]:
                mutations_performed += 1
                mutation_log.append(f"Scalar value changed at index {index2} of constraint {index}")
        elif random_val_replace() == "objective":
            index = random.randint(0, len(objective)-1)
            old_value = objective[index]
            objective[index] = random.randint(0, MAX_INT_32)
            print(objective)
            if old_value != objective[index]:
                mutations_performed += 1
                mutation_log.append(f"Scalar value changed at index {index} of objective")
        
        sys.stdout = open(os.devnull, 'w')
        cplex_obj, cplex_vals = cplex_model(objective, lower_bounds, upper_bounds, names, constraints, constraint_senses, rhs, constraint_names, obj_max)
        grb_obj, grb_vals = grb_model(names, lower_bounds, upper_bounds, constraints, constraint_senses, rhs, objective, obj_max)
        sys.stdout = sys.__stdout__

        print()
        identical = is_identical(cplex_obj, grb_obj, cplex_vals, grb_vals, names)
        print()
        potential_bugs = 0
        if not identical:
            potential_bugs += 1
        print("----------------")

    end_time = time.time()
    total_time = end_time - start_time

    with open(filename, 'w') as file:
        file.write(f"Total Time: {total_time} seconds\n")
        file.write(f"Number of Potential Bugs: {potential_bugs}\n")
        file.write(f"Number of Mutations Performed: {mutations_performed}\n")
        file.write("----------------\n")
        file.write("Mutation Log:\n")
        for mutation in mutation_log:
            file.write(f"{mutation}\n")

    print("Potential Bugs Found:", potential_bugs)


test_linear_prog(num_runs=50, filename="Differential.txt")