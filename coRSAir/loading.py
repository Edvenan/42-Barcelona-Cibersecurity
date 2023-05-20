#!/usr/bin/env python

# Python function called ft_progress(lst) that will display the progress of a for loop via a Loading bar


from time import sleep
from datetime import datetime

# Loading bar function
def ft_progress(lst):

    # Store start time
    t_start = datetime.now()
    
    # Initialize iterations counter and total iterations
    iterations = 0
    total_iterations = len(lst)
    
    # Start the loading bar for each element of the provided list
    for element in lst:
        
        # Provide element to the calling function
        yield element
        
        # Once we come back from calling function:
        # Increment iterations counter
        iterations += 1
        
        # Calculate percentage of progress done
        percentage = (iterations / total_iterations) * 100
        
        # Progress bar: initialization  ('>' equals to 0% < percentage < 5%)
        progress = ""
        
        # Progress bar: update based on percentage completed (one '=' added each additional 5% of progress, for percentage > 5%)
        if int(percentage/5) > 0:
            progress =u"\u2588"*(int(percentage/5))
        
        # Elapsed time calculation
        elapsed_time = (datetime.now()- t_start)
        
        # Estimated time of completion calculation
        eta = elapsed_time * (100 - percentage)/percentage
        
        elapsed_time = str(elapsed_time)[:9]
        eta = str(eta)[:9]
              
        
        # Progress bar printing
        if percentage < 100:
            print("ETA: {:>8} [ {:,.0f}%] [{:<20}] {}/{} | elapsed time {}".format(str(eta), percentage, progress, iterations, total_iterations, str(elapsed_time)), end="\r")
        else:
            # When percentage = 100%, remove leading space of percentage field and Print dotted line 
            print("ETA: {:>8} [{:,.0f}%] [{:<20}] {}/{} | elapsed time {}".format(str(eta), percentage, progress, iterations, total_iterations, str(elapsed_time)), end="\r")
            print("\n...", end='')
        
        

# main function
def main():

    # Example 1
    print("EXAMPLE 1:")
    listy = range(1000)
    ret = 0
    for elem in ft_progress(listy):
        ret += (elem + 3) % 5
        sleep(0.01)
    print()
    print(ret)

    # Example 2
    print()
    print("EXAMPLE 2:")
    listy = range(3333)
    ret = 0
    for elem in ft_progress(listy):
        ret += elem
        sleep(0.005)
    print()
    print(ret)  
  
  
# Executes the main function
if __name__ == '__main__':
    main()