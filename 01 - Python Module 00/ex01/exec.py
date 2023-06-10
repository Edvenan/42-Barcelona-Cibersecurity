#!/usr/bin/env python3

# program that takes a string as argument, reverses it, swaps its letters case and print the result.

import sys

# We store all args in a list
all_args = sys.argv

arguments = (sys.argv)
# If no arguments are provided, do nothing or print an usage
if len(arguments) > 1:

    # We eliminate from the list item 0 (script name)
    arguments = arguments[1:]

    # We create a string made of all args separated by a space
    user_string = ' '.join(arguments)

    # Reverse the string
    reversed_string = user_string[::-1]

    # Swap case of the string
    final_string = reversed_string.swapcase()

    # Print final string
    print(final_string)
