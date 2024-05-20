# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:06:19 2024

@author: loris
"""

from Linear_Programming import Linear_Programming_Testing
from Mixed_Integer_Linear_Programming import Mixed_Integer_Prgramming_Testing
from Quadratic_Programming import Quadratic_Programminng_Testing
from Assignment_Problem import Assignment_Problem_Testing
from Integer_Programming_Knapsack import Integer_Programming_Testing



def Metamorphic_Test_Suite(filename):
    with open(filename, "w") as file:
        file.write("--------------------------------------------------------------\n") 
        file.write("Metamorphic Testing:\n")
        file.write("--------------------------------------------------------------\n") 
    Linear_Programming_Testing(filename)
    Mixed_Integer_Prgramming_Testing(filename)
    Quadratic_Programminng_Testing(filename)
    Assignment_Problem_Testing(filename)
    Integer_Programming_Testing(filename)
    
    
Metamorphic_Test_Suite("Metamorphic.txt")