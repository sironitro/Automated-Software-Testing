# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:31:53 2024

@author: loris
"""

#Imports
from docplex.mp.model import Model
from datetime import datetime
import numpy as np

def Quadratic_Programminng_Testing(filename):
    bug=0
    non_bug=0
    nr_of_runs=1000
    nr_of_constraints=10
    run_counter=0
    
    start = datetime.now()
    #Enviroment
    quadratic_model = Model('quadratic')
    
    for t in range(nr_of_runs):
        
        #Data
        c1=np.random.randint(0,10)
        c2=np.random.randint(c1,20)
        c3=np.random.randint(c2+10,40)
        obj_mul1=np.random.randint(0,10)
        obj_mul2=np.random.randint(0,10)
        obj_mul3=np.random.randint(0,10)
        obj_mul4=np.random.randint(0,10)
        
        #Variables
        x = quadratic_model.continuous_var(name = 'x', lb=0)
        y = quadratic_model.integer_var(name = 'y', lb = 0)
        z = quadratic_model.binary_var(name = 'z')
        
        #Constraint
        quadratic_model.add(x**2 >= c1)
        quadratic_model.add(y**2 >= c2)
        quadratic_model.add(z**2 + y**2 <=c3)
        
        
        #Objective
        obj_fn = obj_mul1*x**2 + obj_mul2*y**2 + obj_mul3*z**2
        quadratic_model.set_objective('min', obj_fn)
        
      
        #Metamophic Testing
        test_quadratic_model = Model('test quadratic')
        
        v1 = test_quadratic_model.continuous_var(name = 'v1', lb=0)
        v2 = test_quadratic_model.integer_var(name = 'v2', lb = 0)
        v3 = test_quadratic_model.binary_var(name = 'v3')
        
        test_quadratic_model.add(v1**2 >= c1)
        test_quadratic_model.add(v2**2 >= c2)
        test_quadratic_model.add(v3**2 + v2**2 <=c3)

        obj_fn = obj_mul4*(obj_mul1*v1**2 + obj_mul2*v2**2 + obj_mul3*v3**2)
        test_quadratic_model.set_objective('min', obj_fn)
        
        for i in range(nr_of_constraints):
            r1=np.random.randint(0,10)
            if(r1 <= c1):
                test_quadratic_model.add( v1**2     >= r1)
            if(r1 <= c2):
                test_quadratic_model.add( v2**2   >= r1)
            if(r1 >= c3):
                test_quadratic_model.add( v3**2 + v2**2   <= r1)
                
        test_quadratic_model.solve()
        quadratic_model.solve()
    
        
        #Comparison
        if((v2.solution_value!=y.solution_value or v2.solution_value!=y.solution_value) and obj_mul1!=obj_mul3 and obj_mul2!=obj_mul3 and obj_mul1!=obj_mul2):
            bug+=1
            print("BUG!")
            test_quadratic_model.print_solution()
            quadratic_model.print_solution()
            test_quadratic_model.clear()
            quadratic_model.clear()
    
        
        else:
            non_bug+=1
            test_quadratic_model.clear()
            quadratic_model.clear()        
    
        run_counter+=1
        print(str(run_counter)+"/"+str(nr_of_runs)+" QP runs completed")
    
            
    print(str(bug)+' bugs during '+str(nr_of_runs)+' runs')
    end=datetime.now()
    duration=end-start
    with open(filename, "a") as file:
        file.write("Quadratic Programming Testing:\n")
        file.write(f"Start Date and Time: {start}\n")
        file.write(f"Number of runs: {nr_of_runs}\n")
        file.write(f"Number of irellevant constrains: {nr_of_constraints}\n")
        file.write(f"{bug} bugs detected during {nr_of_runs} runs\n")
        file.write(f"Total Duration: {round(duration.total_seconds(),2)} seconds \n")
        file.write("--------------------------------------------------------------\n") 
