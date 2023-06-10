#!/usr/bin/env python

# Python program that takes a string S and an integer N as argument and print the list of words in S 
# that contains more than N non-punctuation characters.


import sys
import string

def main():
   
    # Store user arguments in a list
    arguments = sys.argv

    # Check number of arguments provided and if integer
    if len(arguments) != 3:    # num of arguments provided different than 2
        print("ERROR")
    
    else:
        # Store user arguments in variables
        s = arguments[1]
        n = arguments[2]
        
        # Remove punctuation symbols from s using mapping table and translate string method
        s = s.translate(str.maketrans('', '', string.punctuation))

        # Print error and finish either if 1st argument is an integer or if 2nd argument is not an integer. Else, continue.
        if s.isdigit() or not n.isdigit():
            print("ERROR")
        else:
            # Create list of words 'lw' contained in 1st argument
            lw = s.split(" ")
            
            # Convert 2nd argument to int()
            n = int(n)
            
            # Using list comprehension, check length of each word in 1st argument (list 'lw')
            # and add it to 'result' if it's longer than n
            result = [word for word  in lw if len(word)>n]
            
            # print result
            print(result)
            

if __name__ == "__main__":
    main()