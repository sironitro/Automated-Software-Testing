# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:29:11 2024

@author: loris
"""


#Imports
from docplex.mp.model import Model
from datetime import datetime
import numpy as np


def Mixed_Integer_Prgramming_Testing(filename):
    bug=0
    non_bug=0
    nr_of_runs=1000
    nr_of_constraints=100
    run_counter=0
    
    
    start = datetime.now()
    #Enviroment
    milp_model = Model (name = 'MILP')
    
    
    #Data
    
    for t in range(nr_of_runs):
        
        c1=np.random.randint(2,100)
        c2=np.random.randint(c1,200)
        c3=np.random.randint(0,c1-1)
        obj_mul1=np.random.randint(1,10)
        obj_mul2=np.random.randint(1,10)
        
        
        
        #Variables
        x = milp_model.binary_var(name = 'x')
        y = milp_model.continuous_var(name = 'y', lb=0)
        z = milp_model.integer_var(name = 'z', lb=0)
        
        #Constraints
        milp_model.add_constraint(x+2*y  <=c1, ctname = "c1")
        milp_model.add_constraint(2*z+y    <=c2, ctname = "c2")
        milp_model.add_constraint(x+z    <=c3, ctname = "c3")
        
        #Objective
        obj_fn = 2*x+y+3*z
        milp_model.set_objective('max', obj_fn)
        
        
        #Print
        milp_model.solve()
        
        
        #Metamorphic
        
        
        #Test Enviroment
        test_milp_model = Model (name= 'Test MILP')
        
        
        v1 = test_milp_model.binary_var(name = 'v1')
        v2 = test_milp_model.continuous_var(name = 'v2', lb=0)
        v3 = test_milp_model.integer_var(name = 'v3', lb=0)
        
        test_milp_model.add_constraint(v1+2*v2  <=c1)
        test_milp_model.add_constraint(2*v3+v2    <=c2)
        test_milp_model.add_constraint(v1+v3      <=c3)
        
        
            
        for i in range(nr_of_constraints):
            r1=np.random.randint(0,200)
            if(r1 >= c1):
                test_milp_model.add_constraint(v1+2*v2  <=r1)
            if(r1 >= c2):
                test_milp_model.add_constraint(2*v3+v2    <=r1)
            if(r1 >= c3):
                test_milp_model.add_constraint(v1+v3      <=r1)
        
        
        test_obj_fn = obj_mul2*((obj_mul1*2*v1)+(obj_mul1*v2)+(3*obj_mul1*v3))
        test_milp_model.set_objective('max', test_obj_fn)
        
        test_milp_model.solve()
        
        
        #Comparison
        if(v1.solution_value!=x.solution_value or v2.solution_value!=y.solution_value or v3.solution_value!=z.solution_value):
            bug+=1
            print("BUG!")
            test_milp_model.clear()
            milp_model.clear()
    
        else:
            non_bug+=1
            test_milp_model.clear()
            milp_model.clear()
          
        run_counter+=1
        print(str(run_counter)+"/"+str(nr_of_runs)+" runs completed")
    
            
    print(str(bug)+' bugs and '+str(non_bug)+' Non Bugs detected during '+str(nr_of_runs)+' runs')
    end=datetime.now()
    duration=end-start
    with open(filename, "a") as file:
        file.write("Miexed Integer Linear Programming Testing:\n")
        file.write(f"Start Date and Time: {start}\n")
        file.write(f"Number of runs: {nr_of_runs}\n")
        file.write(f"Number of irellevant constrains: {nr_of_constraints}\n")
        file.write(f"{bug} bugs detected during {nr_of_runs} runs\n")
        file.write(f"Total Duration: {round(duration.total_seconds(),2)} seconds \n")
        file.write("--------------------------------------------------------------\n") 

