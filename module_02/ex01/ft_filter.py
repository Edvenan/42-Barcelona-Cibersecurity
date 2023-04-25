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
import traceback

###############################
# FUNCTIONS
###############################

def ft_filter(function_to_apply, iterable):
    """Filter the result of function apply to all elements of the iterable.
        Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
        Return:
        An iterable.
        None if the iterable can not be used by the function.
    """
  
    # validate arguments
    if not function_to_apply or len(iterable) != 1:
        raise TypeError("ft_filter() expected 2 arguments, got ",len(iterable)+1)
    else:
        for iter in iterable:
            if not hasattr(iter, '__iter__'):
                raise TypeError("{} object is not iterable".format(type(iter).__name__))
    
    if not callable(function_to_apply):
        raise TypeError("First argument must be a function.")
    

    # Combine iter arguments in case there are more than one
    iterables = zip(*iterable)
    for iter in iterables:
        if (function_to_apply(*iter)):
            yield 
    