#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:08:02 2021

@author: justice
"""

import numpy as np

'''
This file is used to create the twist distribution array for MachUpX used for the 
Ikhana. This code is specific to the Ikhana.
Also, this code generates the twist distribution such that we get 
rectangular flaps. If you specify the twist distribution as:
     [span_frac, twist]
    ([[0.0, 0],
      [0.2, 1],
      [0.4, 2],                     Linearly Interpolated Example
      [0.6, 3],
      [0.8, 4],
      [1.0, 5]])
    you will get a linear extrapolation between the span fractions you specified. 
    So at a span fraction of 0.1 your twist will be 0.5, at span frac 0.5 your twist
    will be 2.5 and so forth. 
    
    We don't want the linear extrapolation between specified locations. We want 
    rectangular flaps like you would get on an actual airplane. So to do this, we
    needed to double up the span fractions and the twist values, like this:
    ([[0.0, 0],
      [0.0, 1],
      [0.2, 1],
      [0.2, 2],
      [0.4, 2],                     Rectangular Flap Example
      [0.4, 3],
      [0.6, 3],
      [0.6, 4],
      [0.8, 4],
      [0.8, 5],
      [1.0, 5]])
    This way between 0.0 and 2.0 we maintain a constant value of 1. 
    Between 2.0 and 4.0 we maintain a constant value of 2 and so on so forth. 
    
In order to dynamically generate the doubled up span fraction list and the associated
twist's, the following code was written such that the user can specify the desired
number of inboard and outboard flaps. 

Also, the code can be used with scipy.optimize.minimize by using the "create_span_fraction_array"
function at the beginning of the optimization to get the span fraction distribution that
will yield the desired number of inboard and outboard flaps. 

Then each time the optimization runs, call the "double_and_repeat" function to 
get the x array used in scipy.optimize.minimize in the appropriate form. 

Once you have the x array doubled and repeated you can use the "join" function 
to combine the span fraction array with the doubled x array and get your twist
distribution, like that in the Rectangular Flap Example, that can be passed into 
MachUpX. 
'''


def create_span_fraction_array(num_control_points):
    '''This function creates the span fraction array for the NASA Ikhana.
    The user can specify the number of control points and then the span fraction
    array will be created such that there will be rectangular flaps in between 
    each span frac.

    Parameters
    ----------
    num_control_points : int, the number of control points desired

    Returns
    -------
    span_frac_list : list, all of the span fractions necessary to create the 
    desired number of rectangular flaps.

    '''
    max_span_frac = 1.0
    
    step = max_span_frac / num_control_points
    
    span_frac_list = []
    span_frac_list.append(0.0)
    span_frac_list.append(0.0)
    last_frac = 0.0
    
    for x in range(0,num_control_points-1):
        span_frac_list.append(last_frac + step)
        span_frac_list.append(last_frac + step)
        last_frac += step
    
    span_frac_list.append(max_span_frac)
    
    return span_frac_list


def double_and_repeat(array):
    '''This function creates an array twice the length of the orignal by repeating
    each value in the original array. For example: 
        Given:      [1,2,3,4]
        Returns:    [0,1,1,2,2,3,3,4,4]

    Parameters
    ----------
    array : list or array, the original array you want repeated

    Returns
    -------
    doubled_array : list, double the length of original array and with values repeated

    '''
    doubled_array = []
    doubled_array.append(0.0)
    for val in array:
        doubled_array.append(val)
        doubled_array.append(val)
        
    return doubled_array


def join(a, b):
    '''This function takes two strings and merges them together. I wrote it so that 
    I could dynamically create span distributions. The A matrix represents the span
    fractions, and the B matrix represents the twist at that span fraction. The two
    arrays are then combined into the form they need to be in for reading in twist 
    information based on span fraction for MachUpX. For example:
        deflections = {"flaps1" : np.array([[0.0, 0.0],
                                            [0.2, x[0]],
                                            [0.4, x[1]],
                                            [0.6, x[2]],
                                            [0.8, x[3]],
                                            [1.0, x[4]]])}
    
    Parameters
    ----------
    a : list or array, Span Fractions
    b : list or array, twist at the span fraction

    Returns
    -------
    output_array : 2D array for the twist distribution over the span of the wing that can 
    be used in MachUpX

    '''
    length_a = len(a)
    length_b = len(b)
    
    if length_a != length_b:
        return
    else:
        output_array = np.full((length_a,2),0.0)
        for x in range(0,length_a):
            output_array[x][0] = a[x]
            output_array[x][1] = b[x]
            
        return output_array
        
    
def double_repeat_and_join(a, b):
    '''This function combines the double_and_repeat function and the join function.
    The user passes the span fractions in as A and the x array from scipy.optimize.minimize
    in as B. B is doubled and repeated and then joined with A (span_fractions)
    to get the twist distribution array needed for MachUpX.

    Parameters
    ----------
    a : list or array, the span fraction locations for flaps.
    b : list or array, the x array from scipy.optimize.minimize (the twist values
                                                                 for each span_frac)

    Returns
    -------
    array, distribution array containing the span fractions and associated twist for 
    rectangluar flaps.

    '''
    b = double_and_repeat(b)
    return join(a, b)


def span_frac_to_cos_cluster(doubled_span_frac):
    '''This function takes the span fraction list and pulls out only the distinct 
    span fraction locations, minus 0 and 1. This is needed so that the span fraction
    locations can be passed to the cosine clustering in MachUp X.
    
    Example of logic for removing doubled values:
        array Index     0   1   2   3   4   5    
        arrayn value    x   x   y   y   z   z
        iteration
            1           0   1   2   3   4
                        x   y   y   z   z
                        
            2           0   1   2   3
                        x   y   z   z
                        
            3           0   1   2
                        x   y   z

    Parameters
    ----------
    doubled_span_frac : array, the span fraction list with doubles

    Returns
    -------
    doubled_span_frac : array, the span fraction list without doubles, 0, or 1

    '''
    del doubled_span_frac[0] #Remove the first 0.0
    del doubled_span_frac[0] #Remove the second 0.0
    del doubled_span_frac[-1] #Remove the 1.0 at the end of the list
    
    #remove the doubled values
    last_delete = int(len(doubled_span_frac)/2) + 1
    for x in range(1, last_delete):
        del doubled_span_frac[x]
        
    return doubled_span_frac
