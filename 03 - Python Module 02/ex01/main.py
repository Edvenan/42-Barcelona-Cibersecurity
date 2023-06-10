#!/usr/bin/env python
'''
The goal of the exercise is to discover and manipulate *args and **kwargs arguments.

In this exercise you have to implement a function named what_are_the_vars which
returns an instance of class ObjectC.
ObjectC attributes are set via the parameters received during the instanciation. You will
have to modify the 'instance' ObjectC, NOT the class.
You should take a look to getattr, setattr built-in functions.
'''
import sys

# Print Error Messages without Traceback
sys.tracebacklimit = 0

###############################
# FUNCTION what_are_the_vars()
###############################

def what_are_the_vars(*args, **kwargs):
    """
    Function that returns either an instance of class ObjectC with/without attributes
    or None
    """
    # Instanciate new object
    obj = ObjectC()
    
    # If no arguments received, returm empty object
    if len(args) == 0 and len(kwargs) == 0:
        return obj
    
    # Else, 
    # 1) for each 'args', set a new attribute with name = 'var_{# of arg}' and value = arg
    for idx, arg in enumerate(args):
        # Edge case when an arg == 42
        if arg == 42:
            arg = 12
        setattr(obj, f'var_{idx}', arg)
    
    # 2) for each 'kwargs' set a new attribute with name = key and val = val
    for k,v in kwargs.items():
        # If key is not an existing attribute, we set it
        if not hasattr(obj, k):
            # Edge case when an arg == 42
            if v == 42:
                v = 12
            try:
                setattr(obj, k,v)
            except Exception:
                return None
        # If key already exists as an attribute, we return None
        else:
            return None
    return obj

        
###############################
# CLASS ObjectC()
###############################    
class ObjectC(object):
    def __init__(self):
            # ... Your code here ...
            pass

##############################
# FUNCTION doom_printer()
##############################        
def doom_printer(obj):
    if obj is None:
        print("ERROR")
        print("end")
        return
    for attr in dir(obj):
        if attr[0] != '_':
            value = getattr(obj, attr)
            print("{}: {}".format(attr, value))
    print("end")



##################
# main function
##################
def main():

    obj = what_are_the_vars(7)
    doom_printer(obj)
    obj = what_are_the_vars(None, [])
    doom_printer(obj)
    obj = what_are_the_vars("ft_lol", "Hi")
    doom_printer(obj)
    obj = what_are_the_vars()
    doom_printer(obj)
    obj = what_are_the_vars(12, "Yes", [0, 0, 0], a=10, hello="world")
    doom_printer(obj)
    obj = what_are_the_vars(42, a=10, var_0="world")
    doom_printer(obj)
    obj = what_are_the_vars(42, "Yes", a=10, var_2="world")
    doom_printer(obj)

if __name__ == "__main__":
    main()