# Sampling random quantum circuit

**<p style="text-align: center;">This repository hosts the python code required for the final project of the quantum computation and information (PHY733) class given by professor Baptiste Royer at Université de Sherbrooke.</p>**

*<p style="text-align: center;">By Nicolas Mekhaël and Marc-Antoine Roy, Université de Sherbrooke, 10/04/2024</p>*

<div align="center">
  
  <a href="">![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)</a>
  
</div>

## Folder and file description

#### `./figures/`

This folder contains all the figures that the code will output. For example, if the *question #4* requires the output of a figure, this figure will be found in the following folder: `./figures/question4_figs/`.

#### `./tools_for_questions/`

This folder contains all the usefull functions that were used for the project. For example, the functions used to do the wanted computations for *question #4* would be located in the file `./tools_for_questions/question4.py`. There could be some overlap between the files and functions created in `question4.py` could be reused in `question5.py`, as an example.

*<p style="text-align: center;">For each question, further documentation can be found directly in the python files.</p>*

#### `./main_project.py`

In this file, we can easily visualise the result of the computation for a single question. If this file is executed in the terminal, it will run the code for each question and will output the results of the computation. If you wish to exectute only a certain question, you will need to comment certain part of the code. If you wish to modify certain parameters for the simulations, you can do so directly in the `params` python dictionary define at the beginning of this file.

*<p style="text-align: center;">Further explanation can be found directly in the python file.</p>*