# Python function called ft_progress(lst) that will display the progress of a for loop via a Loading bar

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
        progress = ">"
        
        # Progress bar: update based on percentage completed (one '=' added each additional 5% of progress, for percentage > 5%)
        if int(percentage/5) > 1:
            progress ='='*(int(percentage/5)-1) + progress
        
        # Elapsed time calculation
        elapsed_time = (datetime.now()- t_start).total_seconds() 
        
        # Estimated time of completion calculation
        eta = elapsed_time * (100 - percentage)/percentage
        
        # Progress bar printing
        if percentage < 100:
            print("ETA: {:>5,.2f}s [ {:,.0f}%] [{:<20}] {}/{} | elapsed time {:,.2f}s.".format(eta, percentage, progress, iterations, total_iterations, elapsed_time), end="\r")
        else:
            # When percentage = 100%, remove leading space of percentage field and Print dotted line 
            print("ETA: {:>5,.2f}s [{:,.0f}%] [{:<20}] {}/{} | elapsed time {:,.2f}s.".format(eta, percentage, progress, iterations, total_iterations, elapsed_time), end="\r")
            print("\n...", end='')
