


cookbook = {
    'sandwich': {'ingredients':['ham', 'bread', 'cheese', 'tomatoes'], 'meal':'lunch', 'prp_time':15 },
    'cake': {'ingredients':['flour', 'sugar', 'eggs'], 'meal':'dessert', 'prp_time':60 },
    'salad': {'ingredients':['avocado', 'arugula', 'tomatoes', 'spinach'], 'meal':'lunch', 'prp_time':15 },
}

def print_all_names(cookbook):
    print(*[name for name in list(cookbook.keys())], sep='\n')
    return
    

def 



print_all_names(cookbook)