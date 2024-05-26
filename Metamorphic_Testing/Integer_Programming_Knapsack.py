# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:51:51 2024

@author: loris
"""

#Imports
from docplex.mp.model import Model
from datetime import datetime
import numpy as np


def Integer_Programming_Testing(filename):
    bug=0
    non_bug=0
    nr_of_runs=1000
    run_counter=0
    
    
    start = datetime.now()
    #Enviroment
    knapsack_model = Model('Knapsack')
    test_knapsack_model = Model('test Knapsack')
    
    #Data
    for t in range(nr_of_runs):
    
        size=np.random.randint(0,1000)
        r=np.random.randint(1,1000)
        W = list(np.random.randint(0,100,size=size))
        W2 =W+list(np.random.randint(0,100,size=size))
        V = list(np.random.randint(0,100,size=size))
        V2 =V+list(np.random.randint(-100,-1,size=size))
        C = np.random.randint(0,1000)
        N=size
        N2=2*size
        
        #Variables
        x = knapsack_model.binary_var_list(N, name='x')
        v1 = test_knapsack_model.binary_var_list(N2, name='v1')
        
        
        #Constraints
        knapsack_model.add_constraint(sum(W[i]*x[i] for i in range(N)) <= C)
        test_knapsack_model.add_constraint(sum(W2[i]*v1[i] for i in range(N2)) <= C)
        
        
        #Objective
        obj_fn = sum(V[i]*x[i] for i in range(N))
        obj_fn2 = sum(V2[i]*v1[i] for i in range(N2))
        knapsack_model.set_objective('max', obj_fn)
        test_knapsack_model.set_objective('max', r*obj_fn2)
        
        
        knapsack_model.solve()
        test_knapsack_model.solve()
        
        
        #Comparison
        if(round(knapsack_model.objective_value)!=round(test_knapsack_model.objective_value/r)):
            bug+=1
            print("BUG!")
            print(knapsack_model.objective_value,test_knapsack_model.objective_value/r,r)
            knapsack_model.print_solution()
            test_knapsack_model.print_solution()
            knapsack_model.clear()
            test_knapsack_model.clear()
            
    
        
        else:
            non_bug+=1
            knapsack_model.clear()
            test_knapsack_model.clear()    
           
        run_counter+=1
        print(str(run_counter)+"/"+str(nr_of_runs)+" IP runs completed")
            
    print(str(bug)+' bugs during '+str(nr_of_runs)+' runs')      
    end=datetime.now()
    duration=end-start
    with open(filename, "a") as file:
        file.write("Integer Programming Testing:\n")
        file.write(f"Start Date and Time: {start}\n")
        file.write(f"Number of runs: {nr_of_runs}\n")
        file.write(f"{bug} bugs detected during {nr_of_runs} runs\n")
        file.write(f"Total Duration: {round(duration.total_seconds(),2)} seconds \n")
        file.write("--------------------------------------------------------------\n") 

