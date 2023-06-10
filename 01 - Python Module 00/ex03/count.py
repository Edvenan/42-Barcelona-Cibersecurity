#!/usr/bin/env python

# Python function called text_analyzer that takes a single string argument and displays the sums of its
# upper-case characters, lower-case characters, punctuation characters and spaces.

import sys

# Print Error Messages without Traceback
sys.tracebacklimit = 0


# Function text_analyzer

def text_analyzer(my_string=""):

    # Docstring explaining its behavior
    """\n    This function counts the number of upper characters, lower characters,
    punctuation and spaces in a given text."""
    
    # If None or nothing is provided as argument, the user is prompted to provide a string. 
    while (my_string == "" or my_string== None):
        my_string= input('What is the text to analyze?\n')
    
    # If argument is a string, counting proceeds. Else, error is raised.
    if isinstance(my_string, str):
        # Counters creation
        upper_letters  = sum(1 for char in my_string if char.isupper())
        lower_letters  = sum(1 for char in my_string if char.islower())
        punct          = sum(1 for char in my_string if not char.isalnum() and not char.isspace())
        spaces         = sum(1 for char in my_string if char.isspace())
        
        print(f"The text contains {len(my_string)} character(s):")
        print(f"- {upper_letters} upper letter(s)")
        print(f"- {lower_letters} lower letter(s)")
        print(f"- {punct} punctuation mark(s)")
        print(f"- {spaces} space(s)")
    
    else:
        raise AssertionError("argumnet is not a string")


def main():
    
    # store arguments in a list
    arguments = sys.argv

    # check number of arguments provided
    if len(arguments) == 2:         # one argument is provided
        my_argument = arguments[1]
        text_analyzer(my_argument)
    
    elif len(arguments) == 1:
        text_analyzer()
    
    else:
        raise AssertionError("more than one argument are provided")
    

if __name__ == "__main__":
    main()