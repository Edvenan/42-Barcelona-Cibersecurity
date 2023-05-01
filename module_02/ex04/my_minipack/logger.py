#!/usr/bin/env python
""" 
In this exercise, you will learn about decorators and we are not talking about the
decoration of your room. The @log will write info about the decorated function in a
machine.log file.

You have to create the log decorator in the same file. Pay attention to all the different ac-
tions logged at the call of each methods. You may notice the username from environment
variable is written to the log file.

Pay attention, the length between ":" and "[" is 20]. Draw the corresponding conclu-
sions on this part of a log entry
"""
import time
from random import randint
import os
from datetime import datetime

#######################
# DECORATOR
#######################
def log(func):
    # Get env var user
    user = os.getenv("USERNAME", None)
    #user = os.getenv("USER", None)

    def inner(*args):
        # Start time
        start = datetime.now()

        # Call the function
        result = func(*args)
        
        # Elapsed time
        elapsed = datetime.now() - start
        
        # Convert elapsed times to ms or leave it is secs
        elapsed, units = ((elapsed.total_seconds()*1000), "ms") if (elapsed.total_seconds() *1000 < 1) else (elapsed.total_seconds(), "s")
        
        # Get name of called function
        fn = func.__name__.replace("_"," ").capitalize()
        
        # Open log file, append log into file and close file
        f = open("machine.log", "a")
        f.write("({})Running: {:<18} [ exec-time = {:.3f} {} ]\n".format(user, fn, elapsed, units))
        f.close()
        
        return result
    
    return inner


#######################
# CLASS CofeeMachine()
#######################
class CoffeeMachine():
    water_level = 100
    
    @log
    def start_machine(self):
        if self.water_level > 20:
            return True
        else:
            print("Please add water!")
            return False

    @log
    def boil_water(self):
        return "boiling..."

    @log
    def make_coffee(self):
        if self.start_machine():
            for _ in range(20):
                time.sleep(0.1)
                self.water_level -= 1
            print(self.boil_water())
            print("Coffee is ready!")
        
    @log
    def add_water(self, water_level):
        time.sleep(randint(1, 5))
        self.water_level += water_level
        print("Blub blub blub...")
        