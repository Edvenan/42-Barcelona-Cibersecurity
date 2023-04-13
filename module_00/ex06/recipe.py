# initialize and define cookbook as dictionary
cookbook = {
    'sandwich': {'ingredients':['ham', 'bread', 'cheese', 'tomatoes'], 'meal':'lunch', 'prep_time':15 },
    'cake': {'ingredients':['flour', 'sugar', 'eggs'], 'meal':'dessert', 'prep_time':60 },
    'salad': {'ingredients':['avocado', 'arugula', 'tomatoes', 'spinach'], 'meal':'lunch', 'prep_time':15 },
}

# function that prints all recipe names
def print_all_names(cookbook):
    print("\nList of recipes:")
    print(*["   "+name for name in list(cookbook.keys())], sep='\n')
    return cookbook
    
# function that prints a given recipe
def print_recipe(cookbook, name):
    if name in cookbook:
        print(f"\nRecipe for {name}:")
        print('   Ingredients list:',cookbook[name]['ingredients'])
        print('   To be eaten for {}.'.format(cookbook[name]['meal']))
        print('   Takes {} minutes of cooking.\n'.format(cookbook[name]['prep_time']))
    else:
        print(f"\nSorry. The cookbook has no recipe for {name}.")    
    return cookbook

# function that deletes a given recipe
def del_recipe(cookbook, name):
    if name in cookbook:
        del cookbook[name]  
    else:
        print(f"\nSorry. The cookbook has no recipe for {name}.")    
    return cookbook

# function that adds a new recipe to the cookbook
def add_recipe(cookbook):
    name = ''
    while (name ==''):
        name = input('>>> Enter a name:\n')
    
    ingredients = []
    ingredient = ''
    while (ingredient == ''):
        ingredient = input('>>> Enter ingredients:\n')
    
    ingredients.append(ingredient)
    
    while (ingredient != ''):
        ingredient = input()
        if ingredient != '':
            ingredients.append(ingredient)
    
    # enter a meal type
    meal = ''
    while (meal == ''):
        meal = input('>>> Enter a meal type:\n')
    
    # enter prep time  (check if integer?)
    prep_time = ''
    while (prep_time == '' or not prep_time.isdigit()):
        prep_time = input('>>> Enter a preparation time:\n')
    
    # store new recipe in the cookbook
    cookbook[name] = {'ingredients':ingredients, 'meal':meal, 'prep_time':prep_time}

    return cookbook

# Main function
def main():
    
    # User Menu
    print("Welcome to the Python Cookbook !")
    print("List of available option:\n   1: Add a recipe\n   2: Delete a recipe\n   3: Print a recipe\n   4: Print the cookbook\n   5: Quit")
    
    while (True):
        
        option = input("\nPlease select an option:\n>> ")
        match (option):
            case '1':
                add_recipe(cookbook)
            case '2':
                if len(cookbook) > 0:
                    name = ''
                    while (name == ''):
                        name = input("\nPlease enter a recipe name to delete:\n>> ")
                    del_recipe(cookbook, name)
                else:
                    print("\nSorry. The cookbook has no recipes.")
                    
            case '3':
                if len(cookbook) > 0:
                    name = ''
                    while (name == ''):
                        name = input("\nPlease enter a recipe name to get its details:\n>> ")
                    print_recipe(cookbook,name)
                else:
                    print("\nSorry. The cookbook has no recipes.")
            case '4':
                if len(cookbook) > 0:
                    print_all_names(cookbook)
                else:
                    print("\nSorry. The cookbook has no recipes.")
            case '5':
                print("\nCookbook closed. Goodbye !")
                break
            case '':
                print("\r")
            case _ :
                print("\nSorry, this option does not exist")
                print("List of available option:\n   1: Add a recipe\n   2: Delete a recipe\n   3: Print a recipe\n   4: Print the cookbook\n   5: Quit\n")              
                
    return


if __name__ == "__main__":
    main()