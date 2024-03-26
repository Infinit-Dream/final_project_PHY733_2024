"""
Main script for the project
================================================

Contents:
------------------------------------------------
In this file, we first define all the constant parameters that we will need for
each simulations for all the questions. These params are modulable and can be
changed. We also have the main script for the project in order to run the 
functions for each questions that required coding in python. To run a single
question, simply comment out the other questions in the `__main__`. All the
figures produced will be outputed into the folder `./figures/`.

Question 7:
------------------------
All the function used are under `./tools_for_questions/question7.py`. The figure
produced is under `./figures/question7_figs/`.

Question 8:
------------------------
All the function used are under `./tools_for_questions/question8.py`. 

Question 12:
------------------------
All the function used are under `./tools_for_questions/question12.py`. It also
includes the code for the bonus question under 12 labeled question 12.5 in the 
homework. The figure produced is under `./figures/question12_figs/`.

Question 16:
------------------------
All the function used are under `./tools_for_questions/question16.py`. It also
includes the code for the bonus question under 16 labeled question 16.5 in the 
homework. 
"""


import numpy as np
import tools_for_questions.question7 as q7
import tools_for_questions.question8 as q8
import tools_for_questions.question12 as q12
import tools_for_questions.question16 as q16


####################################
#            Parameters            #
####################################

# n: number of qubits, N: number of simulations, c: number of layers
params = {
    "rho_range_q7": (0, 2 * np.pi),
    "phi_range_q7": (0, np.pi),
    "theta_range_q7": (0, 2 * np.pi),
    "n_q7": 1,
    "n_q8": 4,
    "n_q12": 10,
    "max_n_q12_5_bonus": 10,
    "N_q7": 100000,
    "N_q12": 10000,
    "N_q12_5_bonus": 100,
    "c_q12": 5,
    "max_c_q12_5_bonus": 5
}

####################################
#          Run main script         #
####################################

if __name__ == "__main__":
    # Question 7:
    q7.run_q7(params)

    # Question 8:
    q8.run_q8(params)

    # Question 12:
    q12.run_q12(params)

    # Question 12.5 (bonus):
    q12.run_q12_5_bonus(params)