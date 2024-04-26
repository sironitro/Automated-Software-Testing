# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:53:10 2024

@author: loris
"""


bug=0
non_bug=0
nr_of_runs=3000
nr_of_constraints=100


#Enviroment
from docplex.mp.model import Model
opt_mod = Model(name = "Linear Program")


#Data
import numpy as np

for t in range(nr_of_runs):
    c1=np.random.randint(0,10)
    c2=np.random.randint(c1,20)
    c3=np.random.randint(c2,40)
    obj_mul1=np.random.randint(0,10)
    obj_mul2=np.random.randint(0,10)
    
    
    
    
    #Variables
    x=opt_mod.continuous_var(name='x', lb=0)
    y=opt_mod.continuous_var(name='y', lb=0)
    
    #Constraints
    opt_mod.add_constraint( x+y     >= c1,   ctname = 'c1')
    opt_mod.add_constraint( 2*x+y   >= c2,  ctname = 'c2')
    opt_mod.add_constraint( x+4*y   >= c3,  ctname = 'c3')
    
    #Objective
    obj_fn = obj_mul1*x+obj_mul2*y
    opt_mod.set_objective('min', obj_fn)
    
    #Print
    #opt_mod.print_information()
    opt_mod.solve()
    #opt_mod.print_solution()
    
    
    
    #Metamorphic Testing
    
    
    #Test Enviroment
    test_opt_mod = Model(name = "Test Linear Program")
    
    v1=test_opt_mod.continuous_var(name='v1', lb=0)
    v2=test_opt_mod.continuous_var(name='v2', lb=0)
    
    test_opt_mod.add_constraint( v1+v2     >= c1)
    test_opt_mod.add_constraint( 2*v1+v2   >= c2)
    test_opt_mod.add_constraint( v1+4*v2   >= c3)
    
    
    obj_fn = obj_mul1*v1+obj_mul2*v2
    test_opt_mod.set_objective('min', obj_fn)
    
    
    for i in range(nr_of_constraints):
        r1=np.random.randint(0,40)
        if(r1 <= c1):
            test_opt_mod.add_constraint( v1+v2     >= r1)
        if(r1 <= c2):
            test_opt_mod.add_constraint( 2*v1+v2   >= r1)
        if(r1<= c3):
            test_opt_mod.add_constraint( v1+4*v2   >= r1)
            
    #Print
    #test_opt_mod.print_information()
    test_opt_mod.solve()
    #test_opt_mod.print_solution()
    
    
    #Comparison
    if(v1.solution_value!=x.solution_value and obj_mul1!=obj_mul2):
        bug+=1
        print("BUG!")
        test_opt_mod.clear()
        opt_mod.clear()

    else:
        non_bug+=1
        test_opt_mod.clear()
        opt_mod.clear()

        
print(str(bug)+' bugs and '+str(non_bug)+' Non Bugs detected during '+str(nr_of_runs)+' runs')
    
