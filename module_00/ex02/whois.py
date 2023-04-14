#!/usr/bin/env python

# Python program that takes a number as argument, checks whether it is odd, even or
# zero, and prints the result.

import sys

# Print Error Messages without Traceback
sys.tracebacklimit = 0

# store arguments in a list
arguments = sys.argv

# check number of arguments provided and check if it's an integer
if len(arguments) == 2 and arguments[1].isdigit(): # 1 argument provided and it's an integer

    # Conver argument to int
    my_argument = int(arguments[1])

    # check whether the argument is zero or even, else is odd
    if my_argument == 0:
        print("I'm Zero.")
    elif my_argument %2 == 0:
        print("I'm Even.")
    else:
        print("I'm Odd.")
       
elif len(arguments) > 2: # too many arguments provided
    raise AssertionError("more than one argument are provided")

elif len(arguments) == 1: # no arguments provided
    pass

elif not arguments[1].isdigit(): # 1 argument provided but not integer
    raise AssertionError("argument is not an integer")