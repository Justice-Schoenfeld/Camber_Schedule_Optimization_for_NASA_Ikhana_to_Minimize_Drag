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

# Aircraft, Scene, and configuration information
scene_filename = "Ikhana_scene_input.json"
aircraft_json = "Ikhana.json"
aircraft_name = "Ikhana"
num_flaps = 0
upperFlapBound = 25.0
lowerFlapBound = -25.0 

# Create titles for all files, plots, and saved results
title = str(num_flaps) + "_Flaps_"  + aircraft_name + "_CL_0.1_0.9__" + secondsToStr()
deflection_title = title + 'FLAP_DEFLECTIONS'
aoa_title = title + "AOA"
horizontal_stabilizer_title = title + "HS_DEFLECTIONS"
CL_CD_graph_filename = title + ".png"
aoa_graph_title = aoa_title + ".png"
hs_graph_title = horizontal_stabilizer_title + ".png"

# Initialize an array to store all results
results = np.zeros((9,6))

# Loop through Cl = 0.1-0.9 and run the optimization
for lift_coeff in range(1,10):
    CL = lift_coeff/10
    index = lift_coeff - 1
    print("---------- Running CL: " + str(CL) + " ----------")
    
    # Call to optimization code
    dist_filename, CD, act_CL, act_Cm, aoa, elevator, deflections, solutions_array = pitch_trim_flap_optimize_functional(scene_filename, aircraft_json, aircraft_name, num_flaps, CL, upperFlapBound, lowerFlapBound)

    # Store Results
    results[index][0] = CL
    results[index][1] = CD
    results[index][2] = act_Cm
    results[index][3] = aoa
    results[index][4] = elevator
    results[index][5] = act_CL
    
    
# Print out and save results.    
print('CL   CD   Cm   alpha   elevator   act_CL')
print(results)
np.savetxt(title, results, header='CL   CD   Cm   alpha   elevator   act_CL')

# Print out final CL and CD arrays
print('\n------------------------------------')
print("\nCL\n")
print(results[:,0])
print("\nCD\n")
print(results[:,1])


# --- Make and save plots ---
# Plot CL v CD and save
plt.figure(0)
plt.plot(results[:,0], results[:,1])
plt.title(title)
plt.xlabel("CL")
plt.ylabel("CD")
plt.savefig(CL_CD_graph_filename)

# Plot Cl v alpha
plt.figure(1)
plt.plot(results[:,0], results[:,3])
plt.title(aoa_title)
plt.xlabel("CL")
plt.ylabel("Alpha, deg")
plt.savefig(aoa_graph_title)

# Plot CL v Horizontal stabilizer angle
plt.figure(2)
plt.plot(results[:,0], results[:,4])
plt.title(horizontal_stabilizer_title)
plt.xlabel("CL")
plt.ylabel("Horizontal Stabilizer, deg")
plt.savefig(hs_graph_title)