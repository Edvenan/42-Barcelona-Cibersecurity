#!/usr/bin/env python
'''
The goal of the exercise is to work on the built-in functions map, filter and reduce.

Implement the functions ft_map, ft_filter and ft_reduce. Take the time to under-
stand the use cases of these two built-in functions (map and filter) and the function
reduce in functools module. You are not expected to code specific classes to create
ft_map, ft_filter or ft_reduce objects, take a closer look to the examples to know
what to do.

You are expected to produce the raise of exception for the functions similar to ex-
ceptions of map, filter and reduce when wrong parameters are given (but no need to
reproduce the exact the same exception messages).
'''
import sys
from functools import reduce

# Print Error Messages without Traceback
sys.tracebacklimit = 0

###############################
# FUNCTION ft_reduce()
###############################

def ft_reduce(function_to_apply, iterable, initializer=None):
    """Apply function of two arguments cumulatively.
        Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
        Return:
        A value, of same type of elements in the iterable parameter.
        None if the iterable can not be used by the function.
    """
    # validate arguments
    num_arguments = ft_reduce.__code__.co_argcount - len(ft_reduce.__defaults__)
    if (num_arguments != 2):
        raise TypeError("ft_reduce expected 2 arguments, got {}".format(num_arguments))
    else:
        if not callable(function_to_apply):
           raise TypeError("'{}' object is not callable".format(type(function_to_apply).__name__))
        if not hasattr(iterable, '__iter__'):
            raise TypeError("'{}' object is not iterable".format(type(iterable).__name__))

    # Create an iterator object with arg iterable
    it = iter(iterable)
    # Check if initializer arg is passed
    if initializer is None:
        # Assign 1st element of iterator to 'value' and we
        # position 'it's pointer to its second element 
        value = next(it)
    else:
        # Assign initializer to 'value'
        value = initializer

    for element in it:
        value = function_to_apply(value, element)
    return value
    

##################
# main function
##################
def main():

    # Example 1
    x = [1, 2, 3, 4, 5]
    y = (1, 2, 3, 4, 5)
    z = 1
    w =  {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f'}
    lst = ['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']
    
    #############
    # PASS TESTS
    #############
    
    print(ft_reduce(lambda u, v: u + v, lst))
    print(ft_reduce(lambda u, v: u + v, lst, "Welcome " ))
    print(ft_reduce(lambda u, v: u + v, x))
    print(ft_reduce(lambda u, v: u + v, y))
    print(ft_reduce(lambda u, v: u + v, w))
    print(ft_reduce(lambda u, v: u + v, w, 100))
    
    print(reduce(lambda u, v: u + v, lst))    # reduce()
    print(reduce(lambda u, v: u + v, lst, "Welcome " ))    # reduce()
    print(reduce(lambda u, v: u + v, x))    # reduce()
    print(reduce(lambda u, v: u + v, y))    # reduce()
    print(reduce(lambda u, v: u + v, w))    # reduce()
    print(reduce(lambda u, v: u + v, w, 100))    # reduce()
  
    #############
    # FAIL TESTS
    #############
    # 3 arguments
    # print(ft_reduce(lambda dum: not (dum % 2), x, y)))
  
    # one argument only
    #print(ft_reduce(lambda dum: not (dum % 2))))
  
    # no arguments
    #print(ft_reduce()))
    #print(reduce())    #reduce()
  
    # passing a non iterable
    #print(ft_reduce(lambda dum: not (dum % 2), z)))
    #print(reduce(lambda dum: not (dum % 2), z))    #reduce()
  
    # passing a non callable function
    #print(ft_reduce('string', x)))
    #print(reduce('string', x))    #reduce()
  
# Executes the main function
if __name__ == '__main__':
    main()