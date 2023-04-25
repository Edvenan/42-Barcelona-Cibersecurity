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
        raise TypeError("First argument must be a function.")
    for iter in iterable:
    	if not hasattr(iter, '__iter__'):
            #raise TypeError("{} object is not iterable".format(type(iter).__name__))
            print("Error")
            exit(1)
        
    # combine iter arguments in case there are more than one
    iterables = zip(*iterable)
    for iter in iterables:
        try:
            #print(list(function_to_apply(*iter)))
            yield(function_to_apply(*iter))
        except Exception as ex:
            template = "'{0}' exception: {1!s}"
            if (len(ex.args) > 1):
                message = template.format(type(ex).__name__, ex.args)
            else:
                message = template.format(type(ex).__name__, ex.args[0])
            #print(traceback.format_exc())
            print("Function (",function_to_apply.__name__,") has thrown a "+ message)
            # import traceback
            # print traceback.format_exc()
            return None


""" def myfunc(a):
  return len(a)

x = ft_map(myfunc, ('apple', 'banana', 'cherry'))
y = ft_map(lambda x,y,z: x+y+z, ('apple', 'banana', 'cherry'),['apple', 'banana', 'cherry'],"KAS")
print(list(x))   
print(list(y))

num1 = [4, 5, 6]
num2 = [5, 6, 7]

result = ft_map(lambda n1, n2: n1+n2, num1, num2)
print(list(result)) """


a = 4
b = ("Jenny", "Christy", "Monica")
c = ("Monica", "Jenny", "Christy", "Ally")

def myfunc():
    return 4
#ft = ft_map(lambda x,y,z: x+y+z, b, 4)
ft = ft_map(myfunc, 6, 4)
#st = map(3,6,9)
print(list(ft))

'''    
Examples
# Example 1:
x = [1, 2, 3, 4, 5]
ft_map(lambda dum: dum + 1, x)
# Output:
<generator object ft_map at 0x7f708faab7b0> # The adress will be different

list(ft_map(lambda t: t + 1, x))
# Output:
[2, 3, 4, 5, 6]

# Example 2:
ft_filter(lambda dum: not (dum % 2), x)
# Output:
<generator object ft_filter at 0x7f709c777d00> # The adress will be different

list(ft_filter(lambda dum: not (dum % 2), x))
# Output:
[2, 4]

# Example 3:
lst = [’H’, ’e’, ’l’, ’l’, ’o’, ’ ’, ’w’, ’o’, ’r’, ’l’, ’d’]
ft_reduce(lambda u, v: u + v, lst)
# Output:
"Hello world"

'''