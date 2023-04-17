#!/usr/bin/env python

# Python program that allows the user to manage a cookbook of recipes


# Initialize and define cookbook as dictionary
cookbook = {
    'sandwich': {'ingredients':['ham', 'bread', 'cheese', 'tomatoes'], 'meal':'lunch', 'prep_time':15 },
    'cake': {'ingredients':['flour', 'sugar', 'eggs'], 'meal':'dessert', 'prep_time':60 },
    'salad': {'ingredients':['avocado', 'arugula', 'tomatoes', 'spinach'], 'meal':'lunch', 'prep_time':15 },
}


# Function that prints all recipe names
def print_all_names(cookbook):
    print("\nList of recipes:")
    # Print and justify the cookbook recipe names
    print(*["   "+name for name in list(cookbook.keys())], sep='\n')
    return cookbook
    

# Function that prints a given recipe
def print_recipe(cookbook, name):
    # Check if recipe name exists in cookbook. If so, print details. Else, inform user.
    if name in cookbook:
        print(f"\nRecipe for {name}:")
        print('   Ingredients list:',cookbook[name]['ingredients'])
        print('   To be eaten for {}.'.format(cookbook[name]['meal']))
        print('   Takes {} minutes of cooking.\n'.format(cookbook[name]['prep_time']))
    else:
        print(f"\nSorry. The cookbook has no recipe for {name}.")    
    return cookbook


# Function that deletes a given recipe
def del_recipe(cookbook, name):
    # Check if recipe name exists in cookbook. If so, delete it. Else, inform user.
    if name in cookbook:
        del cookbook[name]  
    else:
        print(f"\nSorry. The cookbook has no recipe for {name}.")    
    return cookbook


# Function that adds a new recipe to the cookbook
def add_recipe(cookbook):
    name = ''
    # Ask for recipe name until one is given
    while (name ==''):
        name = input('>>> Enter a name:\n')
    
    ingredients = []
    ingredient = ''
    # Ask for first ingredient until one is given
    while (ingredient == ''):
        ingredient = input('>>> Enter ingredients:\n')
    
    ingredients.append(ingredient)
    # Ask with no prompt for additional ingredients until none is given
    while (ingredient != ''):
        ingredient = input()
        if ingredient != '':
            ingredients.append(ingredient)
    
    # enter a meal type
    meal = ''
    # Ask for meal type until one is given
    while (meal == ''):
        meal = input('>>> Enter a meal type:\n')
    
    # enter prep time
    prep_time = ''
    # Ask for prep time until one is given and is an integer
    while (prep_time == '' or not prep_time.isdigit() or (prep_time.isdigit() and int(prep_time)<0) ):
        prep_time = input('>>> Enter a preparation time:\n')
    
    # store new recipe in the cookbook
    cookbook[name] = {'ingredients':ingredients, 'meal':meal, 'prep_time':prep_time}
    return cookbook

# Main function
def main():
    
    # User Menu
    print("Welcome to the Python Cookbook !")
    print("List of available options:\n   1: Add a recipe\n   2: Delete a recipe\n   3: Print a recipe\n   4: Print the cookbook\n   5: Quit")
    
    # Ask user input until option 5 is chosen
    while (True):
        option = input("\nPlease select an option:\n>> ")
        match (option):
            case '1':       # add recipe
                add_recipe(cookbook)
            case '2':       # del recipe
                # Check if cookbook is empty before calling del_recipe() function
                if len(cookbook) > 0:
                    name = ''
                    while (name == ''):
                        name = input("\nPlease enter a recipe name to delete:\n>> ")
                    del_recipe(cookbook, name)
                else:
                    print("\nSorry. The cookbook has no recipes.")
            case '3':       # print_recipe
                # Check if cookbook is empty before calling print_recipe() function
                if len(cookbook) > 0:
                    name = ''
                    while (name == ''):
                        name = input("\nPlease enter a recipe name to get its details:\n>> ")
                    print_recipe(cookbook,name)
                else:
                    print("\nSorry. The cookbook has no recipes.")
            case '4':       # print all recipe names
                # Check if cookbook is empty before calling print_all_names() function
                if len(cookbook) > 0:
                    print_all_names(cookbook)
                else:
                    print("\nSorry. The cookbook has no recipes.")
            case '5':       # Quit
                print("\nCookbook closed. Goodbye !")
                break
            case '':       # if user inputs ''
                print('',end="\r")
            case _ :       # for any other option that does not exist
                print("\nSorry, this option does not exist.")
                print("List of available option:\n   1: Add a recipe\n   2: Delete a recipe\n   3: Print a recipe\n   4: Print the cookbook\n   5: Quit")

if __name__ == "__main__":
    main()