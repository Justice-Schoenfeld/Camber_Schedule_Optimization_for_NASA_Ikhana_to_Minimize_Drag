# Camber_Schedule_Optimization_for_NASA_Ikhana_to_Minimize_Drag
This repository contains the code used to optimize the NASA Ikhana through camber scheduling to minimized drag used by the author for a master’s thesis as well as work published at AIAA SciTech 2023. The work done focused on minimizing drag by optimizing camber scheduling at various lift coefficients. The optimization is done using the SciPy implementation of Sequential Least Squares Quadratic Programming (SLSQP) combined with a numerical lifting-line method, MachUpX (see https://github.com/usuaero/MachUpX).

Folder Summary
---
* Code
  * Optimization Code 
    * (Code combining SLSQP and MachUpX)
  * Run Code
    * (Code the user will interface with)
* Input Files 
  * (MachUpX input files for the NASA Ikhana with normal tapered wing and modified rectangular wing)

Explanation
---
The Input Files folder contains all the MachUpX required inputs. MachUpX requires an aircraft and scene JSON file in order to run. Included in this repository are input files for the NASA Ikhana as well as a modified version of the NASA Ikhana with a rectangular wing with the same aspect ratio as the normal Ikhana.

The Code folder contains all the python code necessary to conduct and run the optimization. Inside are two sub folders, Optimization Code and Run Code. Optimization Code contains the python code required to perform the actual optimization. Run Code is what the user interfaces with in order to determine the number of control points, the desired lift coefficient, and to specify the MachUpX input files. Inside of the Run Code folder there is an example of running the optimization at a single lift coefficient, over a range of lift coefficients with an initial guess of all zeros, and over a range of lift coefficients with an initial guess based off of the solution for the last lift coefficient.

For a more detailed explanation and to see results obtained with this code for the NASA Ikhana see the authors thesis, https://digitalcommons.usu.edu/etd/8662/.

License
---
This repository is licensed under the MIT license. See LICENSE file for more information.
