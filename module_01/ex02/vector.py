#!/usr/bin/env python

""" In this exercise, you have to create a Vector class. The goal is to create 
vectors and be able to perform mathematical operations with them. """

class Vector:
    
    def __init__(self, values):
        
        # values error handling
        if not isinstance(values, list):
            if isinstance(values, int) and values > 0:
                new_values = []
                for i in range(values):
                    new_values.append([float(i)])
                    
                    values = new_values
                    
            elif isinstance(values, tuple) and isinstance(values[0], int) and\
                isinstance(values[1], int) and values[0]>=0 and values[1]>values[0]:
                    new_values = []
                    for i in range(values[0], values[1]):
                        new_values.append([float(i)])
                    
                    values = new_values
                        
            else:                
                raise TypeError(f"Vector 'values' must be a list or an integer greater than zero.")
        # Column vectors length must be >= 2
        # Row vectors length must be == 1
        
        if len(values) == 1:
            # can be a row vector
            row = values[0]
            if not isinstance(row, list):
                    raise TypeError(f"Row elements must be contained in a list.")
            if len(row) == 0:
                raise ValueError(f"Row vector values cannot be empty.")
            for element in row:
                if not isinstance(element, float):
                    raise TypeError(f"All row vector values must be float.")
            # row vector values initilizattion
            self.values = values
       
        elif len(values) > 1:
            # can be a column vector

            for element in values:
                if not isinstance(element, list):
                    raise TypeError(f"All column vector values must be contained in a list.")
                if len(element) == 0 or len(element) > 1: 
                    raise ValueError(f"All column vector values must be a single float.")
                if not isinstance(element[0], float): 
                    raise TypeError(f"All column vector values must be float.")
            # column vector initilizattion
            self.values = values
        else:
            raise ValueError(f"No values provided at object creation")
         
        # shape initialization        
        self.shape = (len(self.values), len(self.values[0]))
    
    
    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError(f"Both elements must be instances of Vector class.")
        if self.shape != other.shape:
            raise ValueError(f"Both vectors must have the same shape.")

        rows = self.shape[0]
        cols = self.shape[1]
       
        result = 0

        for row in range(rows):
            for col in range(cols):
                result += self.values[row][col] * other.values[row][col]
        return result

    def T(self):
        # Check rows and columns from vector shape
        rows = self.shape[0]
        cols = self.shape[1]

        # Initialize result vector with opposite shape
        result = [[None] * rows] * cols

        # Fill out result vector depending on whether it is a row or a column vector
        if cols == 1:
            # resulting vector will be a row vector (original was column vector [col = 1])
            for row in range(rows):
                for col in range(cols):
                    result[col][row] =  self.values[row][col]
        else:
            # resulting vector will be a column vector (original was row vector [col > 1])
            for row in range(rows):
                for col in range(cols):
                    result[[col][row]] =  [self.values[row][col]]
        return self.__class__(result)    
    
    
    def __add__(self,other):
        if not isinstance(other, Vector):
            raise TypeError(f"Both elements must be instances of Vector class.")
        if self.shape != other.shape:
            raise ValueError(f"Both vectors must have the same shape.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] + other.values[row][col]]
                else:
                    # if row vector
                    result[row][col] = self.values[row][col] + other.values[row][col]
        return self.__class__(result) 
    
    def __radd__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(f"Both elements must be instances of Vector class.")
        if self.shape != other.shape:
            raise ValueError(f"Both vectors must have the same shape.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] + other.values[row][col]]
                else:
                    # if row vector
                    result[row][col] = self.values[row][col] + other.values[row][col]
        return self.__class__(result)  
    
        
    def __sub__(self,other):
        if not isinstance(other, Vector):
            raise TypeError(f"Both elements must be instances of Vector class.")
        if self.shape != other.shape:
            raise ValueError(f"Both vectors must have the same shape.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] - other.values[row][col]]
                else:
                    # if row vector
                    result[row][col] = self.values[row][col] - other.values[row][col]
        return self.__class__(result)  
    
    def __rsub__(self,other):
        if not isinstance(other, Vector):
            raise TypeError(f"Both elements must be instances of Vector class.")
        if self.shape != other.shape:
            raise ValueError(f"Both vectors must have the same shape.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] - other.values[row][col]]
                else:
                    # if row vector
                    result[row][col] = self.values[row][col] - other.values[row][col]
        return self.__class__(result)  
    
    def __mul__(self,other):
        
        if isinstance(other, Vector):
            raise NotImplementedError(f"The __mul__ of two vectors is not implemented")

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f"The escalar must be either a float or an integer.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] * other]
                else:
                    # if row vector
                    result[row][col] = self.values[row][col] * other
        return self.__class__(result)
    
    def __rmul__(self,other):
        if isinstance(other, Vector):
            raise NotImplementedError(f"The __rmul__ of two vectors is not implemented")

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f"The escalar must be either a float or an integer.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] * other]
                else:
                    # if row vector
                    result[row][col] = other * self.values[row][col]
        return self.__class__(result)

    def __truediv__(self,other):
        
        if isinstance(other, Vector):
            raise NotImplementedError(f"The __truediv__ of two vectors is not implemented")
        
        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f"The escalar must be either a float or an integer.")
        if other == 0:
            raise ZeroDivisionError(f"division by zero.")
        
        rows = self.shape[0]
        cols = self.shape[1]
       
        result = [[None] * cols] * rows

        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    # if column vector
                    result[[row][col]] = [self.values[row][col] / other]
                else:
                    # if row vector
                    result[row][col] = self.values[row][col] / other
        return self.__class__(result)

    
    def __rtruediv__(self,other):
        
        if isinstance(other, Vector):
            raise NotImplementedError(f"The __rtruediv__ of two vectors is not implemented")

        raise NotImplementedError(f"Division of a scalar by a Vector is not defined here.")

    def __str__(self):
        return str(self.values)
    
    def __repr__(self):
        # return f"Vector({str(self.values)})"
        return str(self.values)

