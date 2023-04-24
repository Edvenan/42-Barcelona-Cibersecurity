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

###############################
# FUNCTIONS CLASS
###############################

def ft_map(function_to_apply, iterable, *args):
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
        raise TypeError("First argument must be a function.")
    if not hasattr(iterable, '__iter__'):
        raise TypeError("Second argument must be an iterable.")
    
    result = []
    for item in iterable:
        try:
            result.append(function_to_apply(item,*args))
        except Exception as ex:
            template = "'{0}' exception: {1!s}"
            message = template.format(type(ex).__name__, ex.args)
            print("Function (",function_to_apply.__name__,") has thrown a "+ message)
            # import traceback
            # print traceback.format_exc()
            return None
    return result

def myfunc(a,*b):
  return len(a)

x = ft_map(myfunc, ('apple', 'banana', 'cherry'), (1,2,3,4))
y = ft_map(lambda x: x+x, ('apple', 'banana', 'cherry'))
print(x)   
print(y)

num1 = [4, 5, 6]
num2 = [5, 6, 7]

result = ft_map(lambda n1, n2: n1+n2, num1, num2)
print(result)



def ft_filter(function_to_apply, iterable):
    """Filter the result of function apply to all elements of the iterable.
        Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
        Return:
        An iterable.
        None if the iterable can not be used by the function.
    """
    # ... Your code here ...
    
def ft_reduce(function_to_apply, iterable):
    """Apply function of two arguments cumulatively.
        Args:
        function_to_apply: a function taking an iterable.
        iterable: an iterable object (list, tuple, iterator).
        Return:
        A value, of same type of elements in the iterable parameter.
        None if the iterable can not be used by the function.
    """
    # ... Your code here ..