## Overview
This repository contains code for executing fuzzing and metamorphic testing on various problems. The tests are designed to identify potential issues and verify the correctness of the software under different conditions. To be able to run the tests Cplex and Gurobi need to be installed for python.

## Running Tests
To run the tests, execute the test_environment.py script.
To test only a subset of the available tests, comment out the unwanted tests in the test_environment.py file.

## Test Results
The results of the tests are output to their respective folders.
Note: Each time the tests are run, the results files are overwritten. To avoid overwriting results that are referred to in the report, they have been renamed as metamorphic_final and fuzzing_final.