#!/usr/bin/env python

'''
The goal of the exercise is to discover 2 useful methods for lists, tuples, dictionnaries
(iterable class objects more generally) named zip and enumerate.

Code a class Evaluator, that has two static functions named zip_evaluate and enumerate_evaluate.
The goal of these 2 functions is to compute the sum of the lengths of every words of
a given list weighted by a list of coefficinents coefs (yes, the 2 functions should do the
same thing).
The lists coefs and words have to be the same length. If this is not the case, the
function should return -1.
You have to obtain the desired result using zip in the zip_evaluate function, and
with enumerate in the enumerate_evaluate function.
'''

class Evaluator:
    
    def zip_evaluate(coefs:list, words:list[str]):
        
        
        if not isinstance(coefs, list):
            # Type error handling
            raise TypeError("Coefs must be a list.")
        elif not isinstance(words, list):
            # Type error handling
            raise TypeError("Words must be a list.")
        elif len(coefs) != len(words):
            # Strings coefs and words have different lengths
            print('-1')
            exit(1)
        elif len(coefs) == 0:
            # Value error handling
            raise ValueError("Both coefs and words lists must have atleast one element.")
        else:
            # Type error handling
            for element in coefs:
                if not isinstance(element, int) and not isinstance(element, float):
                    raise TypeError("All coefs must be numeric.") 
            for element in words:
                if not isinstance(element, str):
                    raise TypeError("All words must be strings.") 
            
            # calculate product sum using zip
            print(sum(x*len(y) for x,y in zip(coefs, words)))
            
    def enumerate_evaluate(coefs:list, words:list[str]):
        if not isinstance(coefs, list):
            # Type error handling
            raise TypeError("Coefs must be a list.")
        elif not isinstance(words, list):
            # Type error handling
            raise TypeError("Words must be a list.")
        elif len(coefs) != len(words):
            # Strings coefs and words have different lengths
            print('-1')
            exit(1)
        elif len(coefs) == 0:
            # Value error handling
            raise ValueError("Both coefs and words lists must have atleast one element.")
        else:
            # Type error handling
            for element in coefs:
                if not isinstance(element, int) and not isinstance(element, float):
                    raise TypeError("All coefs must be numeric.") 
            for element in words:
                if not isinstance(element, str):
                    raise TypeError("All words must be strings.") 
            
            # calculate product sum using enumerate
            print(sum(coefs[idx]*len(word) for idx,word in enumerate(words)))

words = ["Le", "Lorem", "Ipsum", "est", "simple"]
coefs = [1.0, 2.0, 1.0, 4.0, 0.5]  

Evaluator.zip_evaluate(coefs, words)
Evaluator.enumerate_evaluate(coefs, words)