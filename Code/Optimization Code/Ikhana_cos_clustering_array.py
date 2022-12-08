#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:42:29 2022

@author: justice
"""

from Ikhana_join import *

def create_cos_cluster_array(num_control_points, print_results = False): 
    '''
    This function can be used to get a cosine clustering array for any given
    number of control points for the NASA Ikhana. This code is used in the main
    optimization code (Ikhaa_update_twist_optimization_conditinoal_functional.py)
    to set the cluster points used for the grid for the Ikhana. This function is needed
    because the cluster points are set dynamically during runtime of the optimization,
    meaning any number of control points can be passed in and this function
    will be used to get the appropriate cluster points.

    Parameters
    ----------
    num_control_points : float
        The number of control points to use for the NASA Ikhana.
    print_results : boolean, optional
        Whether to print out the cluster points, useful for debugging and infomrational purposes. The default is False.

    Returns
    -------
    cos_cluster : array, [float]
        The span fraction array without doubles, 0, or 1

    '''     
    span_frac = create_span_fraction_array(num_control_points)
    cos_clust = span_frac_to_cos_cluster(span_frac)
    
    if print_results:
        print("Ikhana span locations for cos clustering (ie span locations for control points)")
        print(cos_clust)
        
    return cos_clust