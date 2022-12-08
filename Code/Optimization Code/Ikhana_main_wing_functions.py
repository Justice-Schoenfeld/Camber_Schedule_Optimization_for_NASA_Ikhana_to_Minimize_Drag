#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:21:05 2022

@author: justice
"""
from math import pi
'''
These are the functions that are used by MachUpX to get CL, CD, and Cm whenever they
are needed for calculations. The data used to get the coefficients comes from
Hunsaker and Phillips
"Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
AIAA SciTech Forum 
9-13 January 2017, Grapevine Texas
55th AIAA Aerospace Sciences Meeting
'''

def get_Ikhana_CL(**kws):
    c1 = kws.get("trailing_flap_deflection", 0)     # radians  0 is a default value in this syntax
    alpha = kws.get("alpha", 0)                     # radians
    c1_deg = c1 * (180/pi)                          # degrees (treating as camber)
    
    aL0 = get_alpha_L0(c1_deg)                      # radians
    CLa = get_CL_alpha(c1_deg)                      # 1/radians
    
    return CLa*(alpha-aL0)                          # unitless coefficient

def get_Ikhana_CD(**kws):
    c1 = kws.get("trailing_flap_deflection", 0)     # radians
    CL = get_Ikhana_CL()                            # unitless coefficient
    c1_deg = c1*(180/pi)                            # degrees (treating as camber)
    
    CD0 = get_CD0(c1_deg)                           # unitless coefficient
    CD1 = get_CD1(c1_deg)                           # unitless coefficient
    CD2 = get_CD2(c1_deg)                           # unitless coefficient

    return (CD0 + CD1*CL + CD2*CL*CL)               # unitless coefficient

def get_Ikhana_Cm(**kws):
    c1 = kws.get("trailing_flap_deflection", 0)     # radians
    alpha = kws.get("alpha", 0)                     # radians
    c1_deg = c1*(180/pi)                            # degrees (treating as camber)
    
    CmL0 = get_Cm_L0(c1_deg)                        # unitless coefficient
    Cma = get_Cm_alpha(c1_deg)                      # 1/radians
    aL0 = get_alpha_L0(c1_deg)                      # radians
    
    return CmL0 + Cma*(alpha-aL0)                   # unitless coefficient

##############################################################################
# The following formulas are based off of camber as a percentage of the chord.
def get_alpha_L0(c):
    '''
    This is a linear fit for the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting

    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        Value of alpha L0 in Radians.

    '''
    return -0.0183*c - 0.0003                       # radians

def get_CL_alpha(c):   
    '''
    This is an average from the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting


    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        CL_alpha in (1/rad).
    '''
    return 6.257605                                 # 1/radians

def get_CD0(c):
    '''
    This is a parabolic fit for the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting

    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        The unitless value for the coefficient CD0.

    '''
    return 0.0002*(c**2) - (4e-5)*c + 0.0049        # unitless coefficient

def get_CD1(c):
    '''
    This is a linear fit for the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting

    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        The unitless value for the coefficient CD1.

    '''
    return -0.003*c + 0.0002                        # unitless coefficient

def get_CD2(c):
    '''
    This is a parabolic fit for the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting

    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        The unitless value for the coefficient CD2.

    '''
    return 0.0001*(c**2) - 0.0004*c + 0.0095        # unitless coefficient

def get_Cm_L0(c):
    '''
    This is a linear fit for the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting

    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        The unitless value for the coefficient Cm_L0.

    '''
    return -0.0253*c - 0.0004                       # unitless coefficient

def get_Cm_alpha(c):
    '''
    This is an average from the data generated by Hunsaker and Phillips in
    "Aerodynamic Shape Optimization of Morphing Wings at Multiple Flight Conditions"
    AIAA SciTech Forum 
    9-13 January 2017, Grapevine Texas
    55th AIAA Aerospace Sciences Meeting


    Parameters
    ----------
    c : float
        camber as percentage of the chord.

    Returns
    -------
    float
        CM_alpha in (1/rad).

    '''
    return 0.016353333                              # 1/radians