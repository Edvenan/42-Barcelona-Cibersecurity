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

# Print Error Messages without Traceback
sys.tracebacklimit = 0
    
###############################
# FUNCTION ft_map()
###############################

def ft_map(function_to_apply, *iterable):
    """Map the function to all elements of the iterable.
        Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
        Return:
        An iterable.
        None if the iterable can not be used by the function.
    """
    # validate arguments
    if not callable(function_to_apply):
        raise TypeError("'{}' object is not callable".format(type(function_to_apply).__name__))
    if len(iterable) == 0:
        raise TypeError("ft_map must have at least two arguments.")
    else:
        for iter in iterable:
            if not hasattr(iter, '__iter__'):
                raise TypeError("{} object is not iterable".format(type(iter).__name__))

    # Combine iter arguments in case there are more than one
    iterables = zip(*iterable)
    for iter in iterables:
        yield(function_to_apply(*iter))


##################
# main function
##################
def main():

    # Example 1
    x = [1, 2, 3, 4, 5]
    y = (1, 2, 3, 4, 5)
    z = 1
    w =  {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f'}
    str_nums = ["4", "8", "6", "5", "3", "2", "8", "9", "2", "5"]
    string_it = ["processing", "strings", "with", "map"]
    with_spaces = ["processing ", "  strings", "with   ", " map   "]
    
    #############
    # PASS TESTS
    #############
    # 2 arguments (function + iterable)
    print(list(ft_map(lambda dum: dum+1, x)))
    print(list(ft_map(lambda dum: dum+1, y)))
    print(list(ft_map(lambda dum: dum+1, w)))
    print(list(ft_map(int, str_nums)))
    print(list(ft_map(str.capitalize, string_it)))
    print(list(ft_map(str.strip, with_spaces)))
    
    print(list(map(lambda dum: dum+1, x)))    # map()
    print(list(map(lambda dum: dum+1, y)))    # map()
    print(list(map(lambda dum: dum+1, w)))    # map()
    print(list(map(int, str_nums)))           # amp()
    print(list(map(str.capitalize, string_it))) # map()
    print(list(map(str.strip, with_spaces))) # map()
    
    # 4 arguments (function + 3 iterables)
    print(list(ft_map(lambda a,b,c: a+b+c, x, y, w)))
    print(list(ft_map(lambda a,b,c: a-b-c, y, x, w)))
    print(list(ft_map(lambda a,b,c: a*b*c, w, x, y)))
    
    print(list(map(lambda a,b,c: a+b+c, x, y, w)))    # map()
    print(list(map(lambda a,b,c: a-b-c, y, x, w)))    # map()
    print(list(map(lambda a,b,c: a*b*c, w, x, y)))    # map()

    
    #############
    # FAIL TESTS
    #############
    # 3 arguments, 2 expected
    #print(list(ft_map(lambda dum: dum+1, x, y)))
    #print(list(map(lambda dum: dum+1, x, y)))  # map()
     
    # one argument only, expected 2
    #print(list(ft_map(lambda dum: dum+1)))
    #print(list(map(lambda dum: dum+1)))  # map()
    
    # no arguments, expected 2
    #print(list(ft_map()))
    #print(list(map()))    # map()
    
    # passing a non iterable
    #print(list(ft_map(lambda dum: dum+1, z)))
    #print(list(map(lambda dum: dum+1, z)))    # map()
    
    # passing a non callable function
    #print(list(ft_map('string', x)))
    #print(list(map('string', x)))    # map()
    
# Executes the main function
if __name__ == '__main__':
    main()