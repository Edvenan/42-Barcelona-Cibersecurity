#!/usr/bin/env python

# Python program that will ask the user to guess a number between 1 and 99

import random

# Generate the secret number
secret_number = random.randint(1, 99)

# Main function
def main():
    
    # Print game information
    print("This is an interactive guessing game!")
    print("You have to enter a number between 1 and 99 to find out the secret number.")
    print("Type 'exit'to end the game.\nGood luck!\n")
    
    # Attempts counter initialization
    attempts = 0
    
    # Start game loop
    
    while (True):
        # Ask for user input (option)
        option = input("What's your guess between 1 and 99?\n>>> ")

        # If option is an integer, we compare it to the secret number. 
        try:
            option = int(option)
            
            # Increment attempts counter
            attempts += 1
            
            if option not in range(1,100):
                print("Your guess must be between 1 and 99!")
         
            elif option < secret_number:
                print("Too low!")
         
            elif option > secret_number:
                print("Too high!")
            
            elif option == secret_number:
                if secret_number == 42:
                    print("The answer to the ultimate question of life, the universe and everything is 42.")
                if attempts == 1:
                    print("Congratulations, you got it on your first try!")    
                else:
                    print("Congratulations, you've got it!")
                    print(f"You won in {attempts} attempts.")
                break 

                   
        # if option not an int, it produces error so we check whether it's an 'exit' or not a number
        except ValueError:
            if option.lower() == 'exit':
                break
            else:
                print("That's not a number")
                # Increment attempts counter
                attempts += 1
        
    return


if __name__ == "__main__":
    main()