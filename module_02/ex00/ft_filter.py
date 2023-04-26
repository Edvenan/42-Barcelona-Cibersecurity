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
# FUNCTION ft_filter()
###############################

def ft_filter(function_to_apply, *iterable):
    """Filter the result of function apply to all elements of the iterable.
        Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
        Return:
        An iterable.
        None if the iterable can not be used by the function.
    """
    # validate arguments
    num_arguments = ft_filter.__code__.co_argcount + len(iterable)
    if (num_arguments != 2):
        raise TypeError("ft_filter expected 2 arguments, got {}".format(num_arguments))
    else:
        if not callable(function_to_apply):
           raise TypeError("'{}' object is not callable".format(type(function_to_apply).__name__))
        for iter in iterable:
            if not hasattr(iter, '__iter__'):
                raise TypeError("'{}' object is not iterable".format(type(iter).__name__))
    
    # pass each item of the iterable argument to the function_to_apply()       
    for iter in iterable:
        for item in iter:
            if (function_to_apply(item)):
                # if function returns True, we yield the item
                yield item


##################
# main function
##################
def main():

    # Example 1
    x = [1, 2, 3, 4, 5]
    y = (1, 2, 3, 4, 5)
    z = 1
    w =  {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f'}
    
    #############
    # PASS TESTS
    #############
    print(list(ft_filter(lambda dum: not (dum % 2), x)))
    print(list(ft_filter(lambda dum: not (dum % 2), y)))
    print(list(filter(lambda dum: not (dum % 2),w)))
    
    print(list(filter(lambda dum: not (dum % 2), x)))    #filter()
    print(list(filter(lambda dum: not (dum % 2), y)))    #filter()
    print(list(filter(lambda dum: not (dum % 2), w)))    #filter()
    
    #############
    # FAIL TESTS
    #############
    # 3 arguments
    # print(list(ft_filter(lambda dum: not (dum % 2), x, y)))
    
    # one argument only
    #print(list(ft_filter(lambda dum: not (dum % 2))))
    
    # no arguments
    #print(list(ft_filter()))
    #print(list(filter()))    #filter()
    
    # passing a non iterable
    #print(list(ft_filter(lambda dum: not (dum % 2), z)))
    #print(list(filter(lambda dum: not (dum % 2), z)))    #filter()
    
    # passing a non callable function
    #print(list(ft_filter('string', x)))
    #print(list(filter('string', x)))    #filter()
    
# Executes the main function
if __name__ == '__main__':
    main()