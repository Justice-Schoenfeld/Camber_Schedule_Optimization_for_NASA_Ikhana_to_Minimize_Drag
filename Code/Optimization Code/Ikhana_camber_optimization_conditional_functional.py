#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:53:39 2021

@author: Justice Schoenfeld
"""

import machupX as mx
import numpy as np
import matplotlib.pyplot as plt
import json
import scipy as sp
import copy
import jsonpickle
from Ikhana_join import create_span_fraction_array, double_repeat_and_join
from airfoil_functional_creation import create_Ikhana_airfoils_function_dict
from Ikhana_cos_clustering_array import create_cos_cluster_array
import timing
from timing import secondsToStr


def pitch_trim_flap_optimize_functional(orig_scene_filename, orig_aircraft_json_filename, aircraft_name, num_flaps, CL_to_set, upDeflBound, lowDeflBound, run_mult_solutions = False, initial_defl = None, dragType = "Total", write_results = True, print_results = False, show_plots = False, dump_forces_and_moments = False):
    '''
    This code is used to pitch trim the given aircraft and then find the minimum drag 
    at the specified lift coefficient using the SLSQP method to minimize the drag value
    returned from the MachUpX forces and moments calculation. This code has the capability to
    re-run a solution multiple times until the difference between consecutive solutions is below
    an error threshold (similar to Optix, see note below with run_mult_solutions flag).
    
    This code will also write the results obtained out to txt files for saving and data
    analysis. 
    
    Once the MachUpX files are read in and MachUpX scene class has been created, the aircraft
    in the scene class is manipulated to get to the trimmed state, then the optimization is run.
    
    The first part of this function is administrative: creating filenames, getting the scene
    class set up and properly configured, creatign the initial x array to be passed to 
    scipy.optimize.minimize, etc..
    
    Then the actual optimization function is defined, followed by the cost function
    definition. The cost function is used in the scipy.optimize.minimize call.
    
    After the cost function, this function extracts the needed reporting information:
        - angle of attack
        - elevator mounting angle
        - CD, CL, Cm
    and creates the output text files for saving the results of the optimization.

    Parameters
    ----------
    orig_scene_filename : string
        Filename of the aircraft scene json.
    orig_aircraft_json_filename : string
        Filename of the aircraft json.
    aircraft_name : string
        Name of the aircraft as given for the 'tag' in the aircraft scene json.
    num_flaps : float
        Desired number of flaps/control points to be used.
    CL_to_set : float
        Desired lift coefficient.
    upDeflBound : float
        Upper bound on the elevator and angle of attack deflections.
    lowDeflBound : float
        Lower bound on the elevator and angle of attack deflections.
    run_mult_solutions : boolean, optional
        Whether or not to take the solution from scipy.optimize.minimize and plug it back in as an initial guess before this function returns. The default is False.
    initial_defl : array, [float], optional
        An array of the initial deflections for the optimization. Length should be = num_flaps + 2 (ie: 4 control points would give [x, x, x, x, x, x]). The default is None.
    dragType : string, optional
        What type of Drag to use ('Total', 'Inviscid', or 'Viscous'). The default is "Total".
    write_results : boolean, optional
        Whether or not to write the results out to files. The default is True.
    print_results : boolean, optional
        Whether or not to print out results to the console. The default is False.
    show_plots : boolean, optional
        Whether or not to show a plot of the normalized lift distribution. The default is False.
    dump_forces_and_moments : boolean, optional
        Whether or not display forces and moments in nice json format. The default is False.

    Returns
    -------
    distributions_filename : string
        The filename for the distributions file, returned so that it can be passed to a function that generates the lift distribution.
    CD : float
        The value of the drag coefficient from the MachUpX calcuated forces and moments.
    fm_CL : float
        The lift coefficient from the MachUpX calculated forces and moments.
    fm_Cm : float
        The pitching moment coefficient from the MachUpX calculated forces and moments.
    aoa : float
        The angle of attack (deg) needed to pitch trim the aircraft.
    elevator : float
        The horizontal stabilizer rotation angle (deg) needed to pitch trim the aircraft usign an all flying tail.
    deflection_array : array, [float]
        The deflections used to achieve the minimum drag at the desired lift coefficient.
    solution.x : array, [float]
        The solution x array from scipy.optimize.minimize. Inlcudes the deflections as well as the elevator and angle of attack values.
    '''
    if (dragType != "Total") and (dragType != "Inviscid") and (dragType != "Viscous"):
        print("Invalid dragType entered! Drag Type must be either 'Total' (default), 'Inviscid', or 'Viscous'.")
        return ''
    
    # --- Create Filenames ---
    partitioned_file_name = orig_scene_filename.partition('.')
    output_title = str(num_flaps) + "_FLAPS_" + partitioned_file_name[0] + "_CL_" + str(CL_to_set) + "__" + secondsToStr() 
    force_moment_output_filename = "F_M_" + output_title + ".json"
    distributions_filename = "distributions_" + output_title
    
    # --- If not Base Case (0 control points) then create span fraction array ---
    if (num_flaps > 0):
        span_frac_array = create_span_fraction_array(num_flaps)
    
    length_x_array = num_flaps + 2    # Number of control points + elevator + alpha
    end_flap_index = num_flaps        # Index of last control point in x array
    elevator_index = num_flaps        # Index of the elevator value in x array
    aoa_index = length_x_array - 1    # Index of the aoa value in x array
       
    
    # Create unique scene and aircraft jsons for the given CL
    scene_filename = str(CL_to_set) + "_" + orig_scene_filename

    
    # Create aircraft dictionary
    orig_aircraft_dict = json.load(open(orig_aircraft_json_filename))
    
    # If not the Baseline case (0 control points) then set cosine clustering points and functions for CD, CL, Cm
    if (num_flaps > 0):
        # Set the cosine clustering points for the number of inboard and outboard flaps
        orig_aircraft_dict['wings']['main_wing']['grid']['cluster_points'] = create_cos_cluster_array(num_flaps)
    
        # Replace airfoil poly_fits with function calls (functional)
        orig_aircraft_dict['airfoils'] = create_Ikhana_airfoils_function_dict()
    
    # Create scene dictionary
    orig_scene_dict = json.load(open(orig_scene_filename))   
    
    # Load state from scene json & save original horizontal tail twist
    scene_state_dict = copy.deepcopy(orig_scene_dict)["scene"]["aircraft"][aircraft_name]["state"]
    orig_aircraft_horizontal_twist = copy.deepcopy(orig_aircraft_dict)["wings"]["horizontal_tail"]["twist"]
    
    # Remove the aircraft so that I can add the aircraft dictionary with functions
    scene_dict = copy.deepcopy(orig_scene_dict)
    scene_dict['scene']['aircraft'].pop(aircraft_name)
    
    # --If desired, format and print the json after changes have been made. Not currently used, but wanted to keep functionality.
    # def notSerializable(thingToPickle):
    #     name = jsonpickle.encode(thingToPickle)
    #     return name
    
    # print(json.dumps(scene_dict, indent = 4))
    # print("\n\n------------------------")
    # print(json.dumps(orig_aircraft_dict, indent = 4, default = notSerializable))
    # print("\n\n------------------------")
    
    
    # Create scene and add scene with functions for airfoils
    my_scene = mx.Scene(scene_dict)
    my_scene.add_aircraft(aircraft_name, orig_aircraft_dict, scene_state_dict)
    
    # --Can be used to display wireframe of aircraft if so desired. Not currently used, but wanted to keep functionality.
    #my_scene.display_wireframe()
    
    # Declaration of optimization function, this function makes the call to scipy.optimize.minimize
    def optimize_twist_with_pitch_trim(CL_to_set):
        '''
        This is the actual function where the drag is minimized. All of the set up has been
        done prior to this point. This function then sets up the bounds and constriants for the
        optimization and makes the call to the scipy.optimize.minimize method. 
        
        After the minimization has happend, this function can plug the solution back into 
        the minimzation if so desired and do so iteratively until the new solution is within 
        a given error margin of the old solution (the solution has converged). This functionality 
        was inspired by Dr Hunsaker and Optix. 
        
        Once a final solution has been achieved, the settings needed for the final 
        solution are returned from this function so that the final results can be 
        calculated and returned to the user.
        
        ** This function MUST stay within the pitch_trim_flap_optimize_functional
           function because of how the scene class in MachUpX works. This function is 
           inside of the parent function so that the scene class is within scope. If it 
           were to be moved otuside of the parent class it is not possible to keep
           the MachUpX scene class in scope and this code would break.

        Parameters
        ----------
        CL_to_set : float
            The desired CL to solve for the minimum drag coefficient.

        Returns
        -------
        solution : OptimizeResult object
            An OptimizeResult object containing the result of the minimization.
        deflection_array : array, [float]
            An array of the camber deflections.
        forces_and_moments : dictionary
            A dictionary of all forces and moments calcuated by MachUpX.
        CD : float
            The value of the drag coefficient calculated using MachUpX's forces and moments solver.
        aoa : float
            The angle of attack (deg) needed to pitch trim the aircraft.
        elevator : float
            The horizontal stabilize mounting angle (deg) needed to pitch trim the aircraft with an all moving tail.
        twist_data_post_solution : array, [[float], [float]]
            A (nx2 array (2D) [span location, twist] with the updated twist used to change the mounting angle (deg) on the horizontal stabilizer in order to pitch trim the aircraft.
        calc_CL : float
            The lift coefficient from the MachUpX calculated forces and moments.
        calc_Cm : float
            The pitching moment coefficient from the MachUpX calculated forces and moments.

        '''
        # Whether to use zeros as initial guess or the passed in initial deflections as the initial guess
        if initial_defl is None: # If no initial_defl given use 0 as initial guess
            x = np.zeros(length_x_array) # Flaps, Elevator, Alpha
        else: # Use the initial deflections given as the initial guess, if of proper size (num_flaps + 2).
            if len(initial_defl) == length_x_array:
                print('Initial Deflections: \n')
                print(initial_defl)
                print('\n')
                x = initial_defl
            else: # initial_defl given is of improper length and CANNOT be used.
                print("Invalid initial_deflection array.\n")
                print("Length needs to be " + str(length_x_array) + "\n")
                print("Entered length is " + str(len(initial_defl)))
                return
        
        # Set the bounds for the optimization. Bounds apply to elevator and angle of attack
        lowerBoundsArray = np.ones(length_x_array)*lowDeflBound
        lowerBoundsArray[elevator_index] = -np.inf
        lowerBoundsArray[aoa_index] = -np.inf
        
        upperBoundsArray = np.ones(length_x_array)*upDeflBound
        upperBoundsArray[elevator_index] = np.inf
        upperBoundsArray[aoa_index] = np.inf
        
        bnds = sp.optimize.Bounds(lowerBoundsArray, upperBoundsArray, keep_feasible = True)
        
        # Set the constraints necessary to pitch trim the aircraft. The constraints are on CL and Cm
        constr1 = {"type" : "eq",
                  "fun" : twist_cost_function,
                  "args" : (CL_to_set, "moment")}
        constr2 = {"type": "eq",
                   "fun" : twist_cost_function,
                   "args" : (CL_to_set, "lift")}
        constr = [constr1, constr2]
        
        # --- CALL TO OPTIMIZATION ---
        solution = sp.optimize.minimize(twist_cost_function, x, args = (CL_to_set), bounds = bnds, constraints = constr)
        
        # Plug the solution back in as initial guess and re-run optimization if desired. (THis functionality mimics Optix)
        if run_mult_solutions:
            epsilon = 5.0; # Error inital value
            prev_solution = solution
            x = prev_solution.x
            run_mult_iter = 1
            print("Iteration " + str(run_mult_iter) + "\n")
            print(str(solution) + "\n\n")
            # Run until the difference in solutions is smaller than 0.0001
            while(abs(epsilon) > 0.0001): # By using the norm of the epsilon vector a threshold of 0.0001 requires all individual differences be at or below 1e-5
                run_mult_iter += 1
                solution = sp.optimize.minimize(twist_cost_function, x, args = (CL_to_set), bounds = bnds, constraints = constr)
                epsilon = np.linalg.norm(prev_solution.x - solution.x)
                prev_solution = solution
                x = solution.x 
                print("Iteration " + str(run_mult_iter) + "\n")
                print(str(solution) + "\n\n")
                
                '''
                The if statement and while loop above help ensure that we have actually reached the minimum value with the optimization.
                The optimization is currently running a SLSQP with bounds. As part of the SLSQP scheme the first derivative is calculated 
                directly and then the differences in the first derivative are used to calculate the second derivative. 
                
                Calculating the second derivative in this manner means that error builds up in the Jacobian inside the SLSQP optimization 
                and the result may not be the actual minimum. By taking the first solution and plugging it back in as the initial guess for
                a second optimization essentially clears the error from the optimization and the optimization starts from the previous result. 
                Then by comparing the solutions and setting a threshold for the difference between two consecutive solutions I can run the 
                optimization as many times as necessary, each time starting at the result of the previous solution, to get to what is the "true"
                solution where my result between optimization runs isn't changing significantly.
                
                This was suggested by Dr Hunsaker and is similar to what he implemented in Optix, which is written for Fortran.
                '''
        
        # Store the angle of attack and elevator deflections
        aoa = solution.x[aoa_index]                                                 # deg
        elevator = solution.x[elevator_index]                                       # deg
        
        # --- Update the twist on the horizontal tail by changing the mounting angle
        aircraft_dict_post_solution = copy.deepcopy(orig_aircraft_dict)
        
        # Add to the mounting angle
        twist_data_post_solution = copy.deepcopy(orig_aircraft_horizontal_twist)
        for row in range(0,len(twist_data_post_solution)):
            twist_data_post_solution[row][1] += elevator                            # deg
            
        # Update the twist in the aircraft dictionary
        aircraft_dict_post_solution["wings"]["horizontal_tail"]["twist"] = twist_data_post_solution
       
        # Update the angle of attack in the scene state
        scene_state_dict["alpha"] = aoa                                             # deg
        
        # Re-initialize MachUpX with new angle of attack and "twist" (tail mounting angle)
        my_scene = mx.Scene(scene_dict)
        my_scene.add_aircraft(aircraft_name, aircraft_dict_post_solution, scene_state_dict)

        deflection_array = []
        if(num_flaps > 0):
            deflection_array = double_repeat_and_join(span_frac_array, solution.x[0:end_flap_index])
            deflections = {"flaps1" : deflection_array}
            my_scene.set_aircraft_control_state(control_state = deflections)        # deg
        
        # Calculate Forces & Moments as well as the Distributions and save the results
        forces_and_moments = my_scene.solve_forces(filename = force_moment_output_filename)
        my_scene.distributions(filename = distributions_filename)
    
        # Get the CL and Cm values and print them. They will only be printed at the end of each CL that is run, if run in a loop.
        calc_CL = forces_and_moments[aircraft_name]['total']['CL']
        calc_Cm = forces_and_moments[aircraft_name]['total']['Cm']
        print("CL: " + str(forces_and_moments[aircraft_name]["total"]["CL"]))
        print("Cm: " + str(forces_and_moments[aircraft_name]["total"]["Cm"]))
    
        # Get the correct drag value from the forces and moments
        if dragType == "Inviscid":
            CD = forces_and_moments[aircraft_name]["inviscid"]["CD"]["total"]
        elif dragType == "Viscous":
            CD = forces_and_moments[aircraft_name]["viscous"]["CD"]["total"]
        else:
            CD = forces_and_moments[aircraft_name]["total"]["CD"]

        # Plot normalized washout with respect to span location if desired.
        if show_plots:
            ''' Plot normalized washout from optimization. Normalize w/ respect to last deflection (-1 index)'''
            span_locations = deflections["flaps1"][:,0]             # Get the span locations that correspond to deflections
            normalized_deflections = deflections["flaps1"][:,1]     # Gets all deflections
            normalized_deflections /= normalized_deflections[-1]    # Normalizes w/ respect to last deflection
    
            plt.plot(span_locations, normalized_deflections, label = "Optimized Values")
            plt.show()
       
        # Return the results of the optimization at the given CL
        return solution, deflection_array, forces_and_moments, CD, aoa, elevator, twist_data_post_solution, calc_CL, calc_Cm
       
        
    ''' Optimizer function for minimizing drag by "twisting" the wing '''
    def twist_cost_function(x, desired_CL ,flag = "drag"):
        '''
        The cost function to be optimized in order to minimize drag. Also used for
        the constraints.
        
        This function can be used for the constriants to change the horizontal 
        stabilizer mounting angle and angle of attack (both in degrees) in 
        order to pitch trim the aircraft. 
        
        Or this function can be used to find the drag coefficient to be minimized. 
        When the drag coefficient is found with this function, it's value is scaled
        by 100.0. This was done because it was found that the CL constraint could
        dominate the minimzation, since the CL is often 1 to 2 orders of magnitude 
        larger than CD. By scaling the drag coefficient it brings the CD value closer
        to the order of magnitude of CL and it was found that better results were obtained.
        
        ** This function MUST stay within the pitch_trim_flap_optimize_functional
           function because of how the scene class in MachUpX works. This function is 
           inside of the parent function so that the scene class is within scope. If it 
           were to be moved otuside of the parent class it is not possible to keep
           the MachUpX scene class in scope and this code would break.

        
        Parameters
        ----------
        x : array, [float]
            x array from scipy.optimize.minimize.
        desired_CL : float
            The desired lift coefficient.
        flag : string, optional
            Which value to return, either 'drag', 'lift', or 'moment'. The default is "drag".

        Returns
        -------
        value : float
            The value of CL, Cm, or CD depending on the flag that was given. (**Note CD will be scaled by 100.0 to bring to same order of magnitude as CL constraint) 

        '''
        # --- Update the twist on the horizontal tail by changing the mounting angle
        aircraft_dict = copy.deepcopy(orig_aircraft_dict)
        
        # Pull in original twist info and add new optimized mounting angle
        twist_data = copy.deepcopy(orig_aircraft_horizontal_twist)
        for row in range(0,len(twist_data)):
            twist_data[row][1] += x[elevator_index]                                 # deg
        
        # Set new twist
        aircraft_dict["wings"]["horizontal_tail"]["twist"] = twist_data
        
        # --- Set the angle of attack
        scene_state_dict["alpha"] = x[aoa_index]                                    # deg
        
        # Re-initialize MachUpX with new "twist" (tail mounting angle)
        my_scene = mx.Scene(scene_dict)
        my_scene.add_aircraft(aircraft_name, aircraft_dict, scene_state_dict)
        
        # --- Change the flap deflections if num_flaps > 0
        if (num_flaps > 0):
            deflection_array = double_repeat_and_join(span_frac_array, x[0:end_flap_index])
            deflections = {"flaps1" : deflection_array}
            my_scene.set_aircraft_control_state(control_state = deflections)        # deg
        
        # Call for forces and moments to get CL and Cm for constraints or CD for value to minimize.
        forces_and_moments = my_scene.solve_forces(verbose=False)
        
        # Get the appropriate value (either a constraint or the minimization value)
        if flag == "moment": # Get Cm for constraint
            value = forces_and_moments[aircraft_name]["total"]["Cm"]
        elif flag == "lift": # Get CL for constraint
            temp_value = forces_and_moments[aircraft_name]["total"]["CL"]
                
            value = abs(temp_value - desired_CL)
        else: # Return CD
            if dragType == "Inviscid":
                value = forces_and_moments[aircraft_name]["inviscid"]["CD"]["total"]
            elif dragType == "Viscous":
                value = forces_and_moments[aircraft_name]["viscous"]["CD"]["total"]
            else:
                value = forces_and_moments[aircraft_name]["total"]["CD"]
            
            # Scale the drag value so that it is on the same order of magnitude as CL and helps the optimization
            value *= 100.0
       
        return value
    
    
    ############################
    ######  Run Analysis  ######
    ############################
    # Get results from the optimization call
    solution, deflection_array, forces_and_moments, CD, aoa, elevator, hs_twist_data, fm_CL, fm_Cm = optimize_twist_with_pitch_trim(CL_to_set)
    
    # Write results out to a file
    if write_results:
        output = open(output_title, 'w')
        
        output.write("CL: " + str(CL_to_set) + "\n")
        if type(initial_defl) != type(None):
            output.write("Initial Defl: " + str(initial_defl) + "\n")
        output.write("Num Flaps: " + str(num_flaps) + "\n")
        output.write("Scene File Name: " + scene_filename + "\n")
        output.write(str(solution) + "\n")
        output.write(str(deflection_array))
        output.write("\n" + dragType + " Drag (CD): " + str(CD) + "\n")
        output.write("Calc CL: " + str(fm_CL) + "\n")
        output.write("Calc Cm: " + str(fm_Cm) + "\n")
        output.write("Angle of Attack: " + str(aoa) + " (deg)\n")
        output.write("Elevator: " + str(elevator) + " (deg)\n")
        output.write("\nHorizontal Stabilizer Twist: \n" + str(hs_twist_data) + "\n")
        if dump_forces_and_moments:
            output.write(json.dumps(forces_and_moments, indent = 4))
        output.close()
        
    # Print results out if so desired.
    if print_results:
        print(solution)
        print("\nDeflection Array: \n")
        print(deflection_array)
        print("\nDrag: ", CD)
        if dump_forces_and_moments:
            print(json.dumps(forces_and_moments, indent = 4))
            
    # Return the any values necessary for looping through multiple CL's
    return distributions_filename, CD, fm_CL, fm_Cm, aoa, elevator, deflection_array, solution.x