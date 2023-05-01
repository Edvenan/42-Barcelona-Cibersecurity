#!/usr/bin/env python
""" 
Objective: Initiation to very basic statistic notions.

Create a class named TinyStatistician that implements the following methods:
    •mean(x): computes the mean of a given non-empty list or array x, using a for-loop.
        The method returns the mean as a float, otherwise None if x is an empty list or
        array. Given a vector x of dimension m x 1, the mathematical formula of its mean
        is:
            
    •median(x): computes the median of a given non-empty list or array x. The method
        returns the median as a float, otherwise None if x is an empty list or array.
    
    •quartiles(x): computes the 1st and 3rd quartiles of a given non-empty array x.
        The method returns the quartile as a float, otherwise None if x is an empty list or
        array.

    •var(x): computes the variance of a given non-empty list or array x, using a for-
        loop. The method returns the variance as a float, otherwise None if x is an empty
        list or array. Given a vector x of dimension m x 1, the mathematical formula of its
        variance is:
            
    •std(x) : computes the standard deviation of a given non-empty list or array x,
        using a for-loop. The method returns the standard deviation as a float, otherwise
        None if x is an empty list or array. Given a vector x of dimension m x 1, the
        mathematical formula of its standard deviation is:

All methods take a list or a numpy.ndarray as parameter.
We are assuming that all inputs have a correct format, i.e. a list or array of numeric type
or empty list or array. You don't have to protect your functions against input errors.
"""
from math import ceil
import numpy

#######################
# CLASS DEFINITION
#######################
 
class TinyStatistician():
    
    def mean(self, lst):
        
        # if input is array, convert to list
        if isinstance(lst, numpy.ndarray):
            lst = list(lst)
        
        # if input is not empty calculate, else return None  
        if lst==[] or lst==[''] or not lst:
            return None
        else:
            mean = sum(x for x in lst)/len(lst)
            return mean
    
    def median(self, lst):
        
        # if input is array, convert to list
        if isinstance(lst, numpy.ndarray):
            lst = list(lst)
        
        # if input is not empty calculate, else return None      
        if lst==[] or lst==[''] or not lst:
            return None
        else:
            #sort the array
            sorted_lst = sorted(lst)
            #number of elements
            ne = len(sorted_lst)
            
            if  ne % 2 ==0:
                # number of elements even
                # avg of the 2 middle elements
                median = (sorted_lst[int((ne/2)-1)]+sorted_lst[int((ne/2))])/2
            else:
                # number of elements odd
                # pick the middle element
                median = float(sorted_lst[int(ne/2)])
            return median
            
    
    def quartiles(self,lst):
        """ 
        https://www.scribbr.com/statistics/quartiles-quantiles/
        """
        # if input is array, convert to list
        if isinstance(lst, numpy.ndarray):
            lst = list(lst)

        # if input is not empty calculate, else return None  
        if lst==[] or lst==[''] or not lst:
            return None
        else:
          
            ne = len(lst)
            sorted_lst = sorted(lst)
            
            # if ne*(1/4) is integer
            if (ne*(1/4) - int(ne*(1/4)) == 0.0):
                q1 = float(sorted_lst[int(ne/4)-1] + sorted_lst[int(ne/4)])/2
            else:
                q1 = float(sorted_lst[int(ceil(ne/4))-1])
            
            # if ne*(3/4) is integer
            if (ne*(3/4) - int(ne*(3/4)) == 0.0):
                q3 = float(sorted_lst[int(ne*(3/4))-1] + sorted_lst[int(ne*(3/4))])/2
            else:
                q3 = float(sorted_lst[int(ceil(ne*(3/4)))-1])

            return [q1, q3]

    def var(self,lst):
        
         # if input is array, convert to list
        if isinstance(lst, numpy.ndarray):
            lst = list(lst)
        
        # if input is not empty calculate, else return None    
        if lst==[] or lst==[''] or not lst:
            return None
        else:
            # number of elements
            ne = len(lst)
            # mean of lst
            lst_mean = self.mean(lst)
            # calc var
            var = sum( (x-lst_mean)**2 for x in lst )/ne
            return var
    
    def std(self, lst):
        # if input is array, convert to list
        if isinstance(lst, numpy.ndarray):
            lst = list(lst)
        
        # if input is not empty calculate, else return None
        if lst==[] or lst==[''] or not lst:
            return None
        else:
           std = self.var(lst)**(0.5)
           return std