# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:06:19 2024

@author: loris
"""

from Metamorphic_Testing.Linear_Programming import Linear_Programming_Testing
from Metamorphic_Testing.Mixed_Integer_Linear_Programming import Mixed_Integer_Prgramming_Testing
from Metamorphic_Testing.Quadratic_Programming import Quadratic_Programminng_Testing
from Metamorphic_Testing.Assignment_Problem import Assignment_Problem_Testing
from Metamorphic_Testing.Integer_Programming_Knapsack import Integer_Programming_Testing
from Differential_Testing.Linear_Programming import test_prog


def Metamorphic_Test_Suite(filename):
    with open(filename, "w") as file:
        file.write("--------------------------------------------------------------\n") 
        file.write("Metamorphic Testing:\n")
        file.write("--------------------------------------------------------------\n") 
    Linear_Programming_Testing(filename)
    print("dones")
    Mixed_Integer_Prgramming_Testing(filename)
    Quadratic_Programminng_Testing(filename)
    Assignment_Problem_Testing(filename)
    Integer_Programming_Testing(filename)

def Differential_Test_Suite(filename):
    with open(filename, "w") as file:
        file.write("--------------------------------------------------------------\n") 
        file.write("Differential Testing:\n")
        file.write("--------------------------------------------------------------\n") 
    test_prog(100, filename, mip=False) # test linear programming
    test_prog(100, filename, mip=True) # test mixed-integer programming
    
Metamorphic_Test_Suite("Metamorphic.txt")
#@Differential_Test_Suite("Differential.txt")
