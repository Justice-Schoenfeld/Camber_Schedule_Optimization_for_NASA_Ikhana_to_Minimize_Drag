#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:40:08 2022

@author: justice
"""
# Get optimization code from different folder
import sys
sys.path.insert(0, '/home/justice/Documents/Thesis/Base-Optimization-Code')
from Ikhana_updated_twist_optimization_conditional_functional import pitch_trim_flap_optimize_functional
import numpy as np

# Set Desired CL
CL = 0.6

# Give aircraft and scene json names as well as aircraft name
scene_filename = "Ikhana_scene_input.json"
aircraft_json = "Ikhana.json"
aircraft_name = "Ikhana"

# Specify number of flaps
num_flaps = 4

# Specify upper and lower bounds for elevator and angle of attack deflections
upperFlapBound = 25.0
lowerFlapBound = -25.0 

# Specify initial guess (number of control points + elevator + angle of attack)
init_guess = np.array([-2.0, -1.0, -2.0, 2.0, -4.0, 3.5])

# Run optimization
dist_filename, CD, act_CL, act_Cm, aoa, elevator, deflections, solution_array = pitch_trim_flap_optimize_functional(scene_filename, aircraft_json, aircraft_name, num_flaps, CL, upperFlapBound, lowerFlapBound, initial_defl=(init_guess))

