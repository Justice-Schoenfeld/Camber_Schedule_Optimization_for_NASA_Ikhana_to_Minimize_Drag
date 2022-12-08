#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:50:03 2022

@author: justice
"""
from CRM_horizontal_stabilizer_functions import *
from CRM_main_wing_functions import *
from Ikhana_main_wing_functions import *

'''
This code is used by to get to create a dictionary used by MachUpX that uses functions
to get CL, CD, and Cm. Passing in functions cannot be set up in the aircraft json before runtime
so it is necessary to read in the aircraft json (making it a dictionary) and then replace 
the airfoils section of the dictionary with output of this function, which now has the 
CL, CD, Cm functions inside of the dictionary.
'''

def create_Ikhana_airfoils_function_dict():
    return {
        "Ikhana_NACA_0010_main": {
		    "type" : "functional",
            "CL" : get_Ikhana_CL,
            "CD" : get_Ikhana_CD,
            "Cm" : get_Ikhana_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr0_xfoil.txt"
			    }
	    },
	    "Ikhana_NACA_0010" : {
    	    "type": "linear",
    	    "aL0": 0.0,
    	    "CLa": 6.43365,
    	    "CmLo": 0.0,
    	    "Cma": 0.0,
    	    "CD0": 0.00513,
    	    "CD1": 0.0,
    	    "CD2": 0.00984
	    }
    }


def create_CRM_airfoils_function_dict():
    return {
	    "uCRM-9_w0": {
		    "type": "functional",
		    "CL" : wr_0_CL,
            "CD" : wr_0_CD,
            "Cm" : wr_0_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr0_xfoil.txt"
			    }
	    },
	    "uCRM-9_w10": {
		    "type": "functional",
		    "CL" : wr_10_CL,
            "CD" : wr_10_CD,
            "Cm" : wr_10_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr10_xfoil.txt"
		    }
	    },
	    "uCRM-9_w15": {
		    "type": "functional",
		    "CL" : wr_15_CL,
            "CD" : wr_15_CD,
            "Cm" : wr_15_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr15_xfoil.txt"
		    }
	    },
	    "uCRM-9_w20": {
		    "type": "functional",
		    "CL" : wr_20_CL,
            "CD" : wr_20_CD,
            "Cm" : wr_20_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr20_xfoil.txt"
		    }
	    },
	    "uCRM-9_w25": {
		    "type": "functional",
		    "CL" : wr_25_CL,
            "CD" : wr_25_CD,
            "Cm" : wr_25_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr25_xfoil.txt"
		    }
	    },
	    "uCRM-9_w30": {
		    "type": "functional",
		    "CL" : wr_30_CL,
            "CD" : wr_30_CD,
            "Cm" : wr_30_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr30_xfoil.txt"
		    }
	    },
	    "uCRM-9_w35": {
		    "type": "functional",
		    "CL" : wr_35_CL,
            "CD" : wr_35_CD,
            "Cm" : wr_35_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr35_xfoil.txt"
		    }
	    },
	    "uCRM-9_w37": {
		    "type": "functional",
		    "CL" : wr_37_CL,
            "CD" : wr_37_CD,
            "Cm" : wr_37_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr37_xfoil.txt"
		    }
	    },
	    "uCRM-9_w40": {
		    "type": "functional",
		    "CL" : wr_40_CL,
            "CD" : wr_40_CD,
            "Cm" : wr_40_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr40_xfoil.txt"
		    }
	    },
	    "uCRM-9_w45": {
		    "type": "functional",
		    "CL" : wr_45_CL,
            "CD" : wr_45_CD,
            "Cm" : wr_45_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr45_xfoil.txt"
		    }
	    },
	    "uCRM-9_w50": {
		    "type": "functional",
		    "CL" : wr_50_CL,
            "CD" : wr_50_CD,
            "Cm" : wr_50_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr50_xfoil.txt"
		    }
	    },
	    "uCRM-9_w55": {
		    "type": "functional",
		    "CL" : wr_55_CL,
            "CD" : wr_55_CD,
            "Cm" : wr_55_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr55_xfoil.txt"
		    }
	    },
	    "uCRM-9_w60": {
		    "type": "functional",
		    "CL" : wr_60_CL,
            "CD" : wr_60_CD,
            "Cm" : wr_60_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr60_xfoil.txt"
		    }
	    },
	    "uCRM-9_w65": {
		    "type": "functional",
		    "CL" : wr_65_CL,
            "CD" : wr_65_CD,
            "Cm" : wr_65_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr65_xfoil.txt"
		    }
	    },
	    "uCRM-9_w70": {
		    "type": "functional",
		    "CL" : wr_70_CL,
            "CD" : wr_70_CD,
            "Cm" : wr_70_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr70_xfoil.txt"
		    }
	    },
	    "uCRM-9_w75": {
		    "type": "functional",
		    "CL" : wr_75_CL,
            "CD" : wr_75_CD,
            "Cm" : wr_75_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr75_xfoil.txt"
		    }
	    },
	    "uCRM-9_w80": {
		    "type": "functional",
		    "CL" : wr_80_CL,
            "CD" : wr_80_CD,
            "Cm" : wr_80_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr80_xfoil.txt"
		    }
	    },
	    "uCRM-9_w85": {
		    "type": "functional",
		    "CL" : wr_85_CL,
            "CD" : wr_85_CD,
            "Cm" : wr_85_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr85_xfoil.txt"
		    }
	    },
	    "uCRM-9_w90": {
		    "type": "functional",
		    "CL" : wr_90_CL,
            "CD" : wr_90_CD,
            "Cm" : wr_90_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr90_xfoil.txt"
		    }
	    },
	    "uCRM-9_w95": {
		    "type": "functional",
		    "CL" : wr_95_CL,
            "CD" : wr_95_CD,
            "Cm" : wr_95_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr95_xfoil.txt"
		    }
	    },
	    "uCRM-9_w100": {
		    "type": "functional",
		    "CL" : wr_100_CL,
            "CD" : wr_100_CD,
            "Cm" : wr_100_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/uCRM-9_wr100_xfoil.txt"
		    }
	    },
        "uCRM-9_h1692": {
		   "type": "functional",
		    "CL" : h1692_CL,
            "CD" : h1692_CD,
            "Cm" : h1692_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h1692.txt"
		    }
	    },
        "uCRM-9_h20": {
		    "type": "functional",
		    "CL" : h20_CL,
            "CD" : h20_CD,
            "Cm" : h20_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h20.txt"
		    }
	    },
        "uCRM-9_h30": {
		    "type": "functional",
		    "CL" : h30_CL,
            "CD" : h30_CD,
            "Cm" : h30_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h30.txt"
		    }
	    },
        "uCRM-9_h40": {
		    "type": "functional",
		    "CL" : h40_CL,
            "CD" : h40_CD,
            "Cm" : h40_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h40.txt"
		    }
	    },
        "uCRM-9_h50": {
		    "type": "functional",
		    "CL" : h50_CL,
            "CD" : h50_CD,
            "Cm" : h50_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h50.txt"
		    }
	    },
        "uCRM-9_h60": {
		    "type": "functional",
		    "CL" : h60_CL,
            "CD" : h60_CD,
            "Cm" : h60_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h60.txt"
		    }
	    },
        "uCRM-9_h70": {
		    "type": "functional",
		    "CL" : h70_CL,
            "CD" : h70_CD,
            "Cm" : h70_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h70.txt"
		    }
	    },
        "uCRM-9_h80": {
		    "type": "functional",
		    "CL" : h80_CL,
            "CD" : h80_CD,
            "Cm" : h80_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h80.txt"
		    }
	    },
        "uCRM-9_h90": {
		    "type": "functional",
		    "CL" : h90_CL,
            "CD" : h90_CD,
            "Cm" : h90_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h90.txt"
		    }
	    },
        "uCRM-9_h100": {
		    "type": "functional",
		    "CL" : h100_CL,
            "CD" : h100_CD,
            "Cm" : h100_Cm,
		    "geometry" : {
			    "outline_points" : "AirfoilDatabase/airfoils/h100.txt"
		    }
	    }
    }