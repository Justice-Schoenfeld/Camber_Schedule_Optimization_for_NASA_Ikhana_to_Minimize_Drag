#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:40:08 2022

@author: justice
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/home/justice/Documents/Thesis/Base-Optimization-Code')
from Ikhana_updated_twist_optimization_conditional_functional import pitch_trim_flap_optimize_functional
from timing import secondsToStr

'''
This code uses the MachUpX/SLSQP optimization code to determing the trimmed drag coefficient
for a range of lift coefficients (CL 0.1 - 0.9). This is done by passing the aircraft and scene
jsons into MachUpX to be initialized. The configuration settings are also specified
(the number of control points (num_flaps), upper bound and lower bound on alpha and horizontal stab deflections)


Then all titles for outputs are generated based off of the aircraft name. The optimization
code is then called in a loop where one lift coefficient is solved at a time. After each lift
coefficient iteration is solved for the drag coefficient then the next lift coefficient is 
passed in and the solution (camber for each control point, horizontal stablizer deflection, angle of attack)
is used as the initial guess for the new lift coefficient.

ie:
    CL 0.1 run with initial guess of all zeros
    -Returns [0.25, 0.25, 0.4, 0.4, 3.26, 5.7]  
    (cp @ 0.0 camber, cp @ 0.5 camber, cp @ 0.5 camber, cp @ 1.0 camber, hs defl in deg, alpha in deg)
    
    then CL 0.2 is run with initial guess of [0.25, 0.25, 0.4, 0.4, 3.26, 5.7]
    - returns xxxxxx
    
    then CL 0.3 is run with initial guess of xxxxxx
    
    and so on until CL 0.9 has been run.
    
After all lift coefficients (CL 0.1 - 0.9) have been run then the process is ran in revers.
Meaning that the program starts at CL 0.8 and solves using the solution from the CL 0.9 iteration.
If the new result is a lower drag coefficient then the new solution replaces the old CL 0.8 solution.
If not then the CL 0.8 solution is unchanged. 

The best result for CL 0.8 (either the first solution, or the new solution achieved with initial guess of CL 0.9 results)
is then used as the initial guess for CL 0.7 and again if the solution is better than the "first" 
CL 0.7 solution the first solution is replaced with the new solution and the process continues all the way to CL 0.1.

**I used "first" when referring to the first solution because it is the result obtained from the 
CL xx iteration of the first for loop in this program. Inside of the optimization in the first 
for loop the optimization process could have been run multiple times. This is because the optimization
code was written in such a way that once the optimization has returned, that solution can immediately
be plugged back into the optimization process as an initial guess. If this is done then the solution 
will be plugged back in until it stops changing within some error limit. This functionality does not have
to be enabled, but it is in this code. So, I used "first" because the "first" solution could have been the
result of multiple optimization calls within the call to the optimization function, but it was the first 
solution returned for the given lift coefficient in this code.

I decided to go "up" from CL 0.1 - 0.9 and then "down" from CL 0.9 - 0.1 to help 
ensure that the results of the optimization didn't get stuck in a local minima. There
were instances before I implemented this up/down approach where looking at the results 
for CL 0.1 - 0.9 it looked like there were almost two different solution valleys achieved.
The first part of the CL v CD curve would be along one parabolic function, then it would 
jump to another parabolic function at some intermediate CL (indicating a different solution valley).

By going up then down it helped get all of the CD values on the same parabolic curve
and in the same solution valley.

'''


# Aircraft, Scene, and configuration information
scene_filename = "Ikhana_scene_input.json"
aircraft_json = "Ikhana.json"
aircraft_name = "Ikhana"
num_flaps = 2
upperFlapBound = 25.0
lowerFlapBound = -25.0  

# Create titles for all files, plots, and saved results
title = str(num_flaps) + "_Flaps_" + aircraft_name + "_CL_0.1_0.9__" + secondsToStr()
deflection_title = title + '__FLAP_DEFLECTIONS'
aoa_title = title + "__AOA"
horizontal_stabilizer_title = title + "__HS_DEFLECTIONS"
solution_array_title = title + "__SOLUTIONS_ARRAY"
changed_title = title + "__CHANGED"

CL_CD_graph_filename = title + ".png"
flap_schedule_graph_filename = deflection_title + ".png"
aoa_graph_title = aoa_title + ".png"
hs_graph_title = horizontal_stabilizer_title + ".png"

# Initialize an array to store all results, previous solutions, and if the solution changed on the second time through
results = np.zeros((9,6))
previous_solution_array = np.zeros((9,num_flaps+2))
has_changed = np.zeros((9,1)) # 0 indicates no change, 1111 indicates change

#--------------------------------  Going "Up"  --------------------------------
# Go through from CL 0.1 to 0.9.
#  For CL 0.1 use initial guess of all 0's. After that, 
#  use the previous CL's solution as the initial guess.
for lift_coeff in range(1,10):
    CL = lift_coeff/10
    index = lift_coeff - 1
    print("---------- Running CL: " + str(CL) + " ----------")
    
    if lift_coeff == 1:
        # Run with NO initial deflections (ie: they will be assumed to be zero)
        dist_filename, CD, act_CL, act_Cm, aoa, elevator, deflections, solution_array = pitch_trim_flap_optimize_functional(scene_filename, aircraft_json, aircraft_name, num_flaps, CL, upperFlapBound, lowerFlapBound, run_mult_solutions=(True))
        prev_solution = solution_array
        previous_solution_array[index,:] = solution_array
    else:
        # Run with initial deflections set to the previous solution (Start at last solution as initial guess)
        dist_filename, CD, act_CL, act_Cm, aoa, elevator, deflections, solution_array = pitch_trim_flap_optimize_functional(scene_filename, aircraft_json, aircraft_name, num_flaps, CL, upperFlapBound, lowerFlapBound, run_mult_solutions=(True), initial_defl=(prev_solution))
        prev_solution = solution_array
        previous_solution_array[index,:] = solution_array
    
    # Store results
    results[index][0] = CL
    results[index][1] = CD
    results[index][2] = act_Cm
    results[index][3] = aoa
    results[index][4] = elevator
    results[index][5] = act_CL
    
    # Store deflections for CL 0.1-0.9
    if (lift_coeff == 1): # Create the all_deflections array
        rows, cols = np.shape(deflections)
        all_deflections = np.zeros((rows, 10))
        all_deflections[:,0:2] = deflections
    else: # Add to the all_deflections array
        # Need to go one above the index (ie: lift_coeff)
        # all_deflectins goes: Span Loc   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9
        all_deflections[:,lift_coeff] = deflections[:,1]
  
# Make and save copies of the original results and deflections
results_from_going_up = results.copy()
deflections_going_up = all_deflections.copy()
orig_prev_solutions_array = previous_solution_array.copy()

results_up_title = title + "__UP"
deflections_up_title = results_up_title + "__deflections"
prev_sol_title = results_up_title + "__orig_solutions"

np.savetxt(results_up_title ,results_from_going_up, header='CL   CD   Cm   alpha   elevator   act_CL')
np.savetxt(deflections_up_title, deflections_going_up, header='Span Loc   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9')
np.savetxt(prev_sol_title, orig_prev_solutions_array, header='Flaps...  Elevator Alpha')



#-------------------------------  Going "Down"  -------------------------------
# Now go from CL 0.9 to CL 0.1 using the "previous" CL's solution as the initial guess.
#  Work way down, if the solution is better than that from going up, then update the results.
#  Also, update the hasChanged array so I know which ones were updated.
for down_num in range(9,1,-1):
    CL = (down_num - 1)/10.0
    down_index = down_num - 1
    CL_index = down_num - 2
    
    # Get results from CL above the CL being run (ie: results for CL 0.9 used for running CL 0.8)
    # Need to use down_index because that is down_num - 1 which will give the prev solution for down_num
    prev_results = previous_solution_array[down_index,:]
    dist_filename, CD, act_CL, act_Cm, aoa, elevator, deflections, solution_array = pitch_trim_flap_optimize_functional(scene_filename, aircraft_json, aircraft_name, num_flaps, CL, upperFlapBound, lowerFlapBound, run_mult_solutions=(True), initial_defl=(prev_results))
    
    # If CD is lower, replace results & deflections
    if (CD < results[CL_index][1]):
        results[CL_index][0] = CL
        results[CL_index][1] = CD
        results[CL_index][2] = act_Cm
        results[CL_index][3] = aoa
        results[CL_index][4] = elevator
        results[CL_index][5] = act_CL
        
        # Update all_deflections.
        # Need to go one above the CL_index to get the proper location (ie: down_index)
        # all_deflectins goes: Span Loc   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9
        all_deflections[:,down_index] = deflections[:,1]
        
        # Update the previous solutions array
        previous_solution_array[CL_index,:] = solution_array
        
        # update the has_changed array to indicate there was a change
        has_changed[CL_index] = 1111

#------------------------------------------------------------------------------
#------------------------  Print & Save Results/Plots  ------------------------
#------------------------------------------------------------------------------

print('CL   CD   Cm   alpha   elevator   act_CL')
print(results)
np.savetxt(title, results, header='CL   CD   Cm   alpha   elevator   act_CL')
np.savetxt(deflection_title, all_deflections, header='Span Loc   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9')
np.savetxt(solution_array_title, previous_solution_array, header='Flaps...  Elevator Alpha')
np.savetxt(changed_title, has_changed, header="CL  Status")

# Print out the CL and CD arrays
print('\n------------------------------------')
print("\nCL\n")
print(results[:,0])
print("\nCD\n")
print(results[:,1])

# Plot CD v CL
plt.figure(0)
plt.plot(results[:,0], results[:,1])
plt.title(title)
plt.xlabel("CL")
plt.ylabel("CD")
plt.savefig(CL_CD_graph_filename)

# Plot Camber schedule for all CL's (0.1-0.9)
plt.figure(1)
plt.plot(all_deflections[:,0], all_deflections[:,1], label = 'CL 0.1')
plt.plot(all_deflections[:,0], all_deflections[:,2], label = 'CL 0.2')
plt.plot(all_deflections[:,0], all_deflections[:,3], label = 'CL 0.3')
plt.plot(all_deflections[:,0], all_deflections[:,4], label = 'CL 0.4')
plt.plot(all_deflections[:,0], all_deflections[:,5], label = 'CL 0.5')
plt.plot(all_deflections[:,0], all_deflections[:,6], label = 'CL 0.6')
plt.plot(all_deflections[:,0], all_deflections[:,7], label = 'CL 0.7')
plt.plot(all_deflections[:,0], all_deflections[:,8], label = 'CL 0.8')
plt.plot(all_deflections[:,0], all_deflections[:,9], label = 'CL 0.9')
plt.title(title)
plt.xlabel('Span')
plt.ylabel("Camber")
plt.legend(loc='right')
plt.savefig(flap_schedule_graph_filename)

# Plot CL v Alpha 
plt.figure(2)
plt.plot(results[:,0], results[:,3])
plt.title(aoa_title)
plt.xlabel("CL")
plt.ylabel("Alpha, deg")
plt.savefig(aoa_graph_title)

# Plot CL v Horizontal stabilizer deflections
plt.figure(3)
plt.plot(results[:,0], results[:,4])
plt.title(horizontal_stabilizer_title)
plt.xlabel("CL")
plt.ylabel("Horizontal Stabilizer, deg")
plt.savefig(hs_graph_title)