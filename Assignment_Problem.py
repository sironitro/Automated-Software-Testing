# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:55:56 2024

@author: loris
"""


bug=0
non_bug=0
nr_of_runs=1000



#Envitorment
from docplex.mp.model import Model
assignment_model = Model('Assignment')
test_assignment_model = Model('Test Assignment')


#Data
import numpy as np

for t in range(nr_of_runs):
    nr_tasks=np.random.randint(1,30)
    nr_workers=nr_tasks
    cost = list(np.random.randint(1,10, (nr_tasks,nr_workers)))
    test_cost=[]
    nr_bad_workers=np.random.randint(1,1000)
    for i in range(nr_tasks):
        test_cost.append(list(cost[i])+list(np.random.randint(11,20,size=nr_bad_workers)))
    
    #Variables
    x = assignment_model.binary_var_matrix(nr_tasks,nr_workers,name='x')
    v1 = test_assignment_model.binary_var_matrix(nr_tasks,nr_workers+nr_bad_workers,name='v1')
    
    
    #Constraints
    assignment_model.add_constraints((sum(x[i,j] for i in range(nr_tasks)) <= 1
                                    for j in range(nr_workers)),
                                    names = 'work_load')
    assignment_model.add_constraints((sum(x[i,j] for j in range(nr_workers)) == 1
                                    for i in range(nr_tasks)),
                                    names = 'task_completion')
    
    
    
    test_assignment_model.add_constraints((sum(v1[i,j] for i in range(nr_tasks)) <= 1
                                    for j in range(nr_workers+nr_bad_workers)),
                                    names = 'test_work_load')
    
    test_assignment_model.add_constraints((sum(v1[i,j] for j in range(nr_workers+nr_bad_workers)) == 1
                                    for i in range(nr_tasks)),
                                    names = 'test_task_completion')
    
    
    #Objective
    obj_fn = sum(cost[i][j]*x[i,j] for i in range(nr_tasks) for j in range(nr_workers))
    test_obj_fn = sum(test_cost[i][j]*v1[i,j] for i in range(nr_tasks) for j in range(nr_workers+nr_bad_workers))
    assignment_model.set_objective('min', obj_fn)
    test_assignment_model.set_objective('min', test_obj_fn)
    
    
    #Print
    assignment_model.solve()
    test_assignment_model.solve()

    
    
    #Comparison
    if(round(assignment_model.objective_value)!=round(test_assignment_model.objective_value)):
        bug+=1
        print("BUG!")
        assignment_model.print_solution()
        test_assignment_model.print_solution()
        assignment_model.clear()
        test_assignment_model.clear()
        
    
    
    else:
        non_bug+=1
        assignment_model.clear()
        test_assignment_model.clear()   
        
        
print(str(bug)+' bugs and '+str(non_bug)+' Non Bugs detected during '+str(nr_of_runs)+' runs')          
