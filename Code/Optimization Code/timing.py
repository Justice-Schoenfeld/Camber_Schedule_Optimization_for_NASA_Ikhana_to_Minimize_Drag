#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 10:00:21 2022

Pulled from stackoverflow on Wed Jan 5, 2022
https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
answered Sep 10 '12 at 2:03 by Nicojo

Used to display the runtime for each of the run code files. It also gives a method
for getting the current time with secondsToStr(), which is used to differentiate
the multiple output files generated during each run.
"""

import atexit
from time import time, strftime, localtime
from datetime import timedelta

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

start = time()
atexit.register(endlog)
log("Start Program")