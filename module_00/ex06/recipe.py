


cookbook = {
    'sandwich': {'ingredients':['ham', 'bread', 'cheese', 'tomatoes'], 'meal':'lunch', 'prep_time':15 },
    'cake': {'ingredients':['flour', 'sugar', 'eggs'], 'meal':'dessert', 'prep_time':60 },
    'salad': {'ingredients':['avocado', 'arugula', 'tomatoes', 'spinach'], 'meal':'lunch', 'prep_time':15 },
}

def print_all_names(cookbook):
    print(*[name for name in list(cookbook.keys())], sep='\n')
    return cookbook
    

def print_recipe(cookbook, name):

    print('   Ingredient list:',cookbook[name]['ingredients'])
    print('   To be eaten for {}.'.format(cookbook[name]['meal']))
    print('   Takes {} minutes of cooking.'.format(cookbook[name]['prep_time']))
    return cookbook

def del_recipe(cookbook, name):
    del cookbook[name]
    return cookbook

def add_recipe(cookbook):
    name = input('Enter a name:\n')
    
    ingredients = []
    
    ingredient = ''
    
    while (ingredient == ''):
        ingredient = input('Enter ingredients:\n')
    
    ingredients += ingredient
    
    while (ingredient != ''):
        ingredient = input()
        if ingredient != '':
            ingredients += ingredient
    
    # enter a meal type
    meal = ''
    while (meal == ''):
        meal = input('Enter a meal type:\n')
    
    # enter prep time  (check if integer?)
    prep_time = ''
    while (prep_time == ''):
        prep_time = input('Enter a preparation time:\n')
    
    cookbook[name] = {}
    return cookbook


print_all_names(cookbook)
print_recipe(cookbook,'cake')
print(del_recipe(cookbook, 'cake'))
print(add_recipe(cookbook))
