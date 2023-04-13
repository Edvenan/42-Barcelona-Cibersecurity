 #!/usr/bin/env python

import sys


def main():
    
    # Print Error Messages without Traceback
    sys.tracebacklimit = 0
    
    # store arguments in a list
    arguments = sys.argv

    # check number of arguments provided and if integer
    if len(arguments) == 1:    # no arguments provided
        print("Usage: python operations.py <number1> <number2>")
        print("Example:\n   python operations.py 10 3")
    
    elif len(arguments) == 2:   # too few arguments
        raise AssertionError("too few arguments")
    
    elif len(arguments) == 3 and arguments[1].isdigit() and arguments[2].isdigit(): # 2 arguments provided and they are integers

        a = int(arguments[1])
        b = int(arguments[2])

        print(f"{'Sum:':<14}{a+b}")
        print(f"{'Difference:':<14}{a-b}")
        print(f"{'Product:':<14}{a*b}")
        try:
            print(f"{'Quotient:':<14}{a/b}")
        except ZeroDivisionError:
            print(f"{'Quotient:':<14}{'ERROR (division by zero)'}")
        try:
            print(f"{'Remainder:':<14}{a%b}")
        except ZeroDivisionError:
            print(f"{'Remainder:':<14}{'ERROR (modulo by zero)'}")
            
    elif len(arguments) > 3:    # too many arguments
        raise AssertionError("too many argumnets")    
    
    else:   # 2 arguments provided but any or all of them not digit
        raise AssertionError("only integers")
    

if __name__ == "__main__":
    main()