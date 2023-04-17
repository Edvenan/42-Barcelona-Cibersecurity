from book import Book
from recipe import Recipe

from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Good Recipes creation tests
recipe1 = Recipe('Lasagna', 3, 30, ['pasta', 'tomatoes', 'minced meat', 'cheese'], 'lunch')
recipe2 = Recipe('Paella', 4, 45, ['rice', 'tomatoes', 'squid', 'peper'], 'lunch', 'Delicious typical Spanish lunch')
recipe3 = Recipe('Salad', 2, 10, ['lettuce', 'tomatoes', 'onion', 'corn'], 'starter')
recipe4 = Recipe('Cake', 5, 60, ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')

# Bad Recipes creation tests

# TEST 1: Missing Data. A 'recipe name' must be provided at object creation
try:
    recipe5 = Recipe('', 5, 60, ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')
except Exception as error: 
    exp_error = "Missing Data. A 'recipe name' must be provided at object creation."
    if str(error) == exp_error and isinstance(error, AssertionError):
        print(bcolors.OKGREEN + "Test 1: OK" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Test 1: NOK" + bcolors.ENDC)


# TEST 2: Invalid Data type. The 'recipe name' must be a string.
try:
    recipe5 = Recipe(1, 5, 60, ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')
except Exception as error:
    print(error) 
    exp_error = "Invalid Data type. The 'recipe name' must be a string."
    if str(error) == exp_error and isinstance(error, AssertionError):
        print(bcolors.OKGREEN + "Test 2: OK" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Test 2: NOK" + bcolors.ENDC)

# TEST 3: Invalid Data type. The 'cooking level' must be an integer.
try:
    recipe5 = Recipe('cake', 'd', 60, ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')
except Exception as error:
    print(error) 
    exp_error = "Invalid Data type. The 'cooking level' must be an integer."
    if str(error) == exp_error and isinstance(error, AssertionError):
        print(bcolors.OKGREEN + "Test 3: OK" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Test 3: NOK" + bcolors.ENDC)



#recipe5 = Recipe('Cake', 6, 60, ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')

#recipe5 = Recipe('Cake', 5, 'd', ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')
#recipe5 = Recipe('Cake', 5, -5, ['flour', 'eggs', 'milk', 'chocolate'], 'dessert')

#recipe5 = Recipe('Cake', 5, 60, [], 'dessert')
#recipe5 = Recipe('Cake', 5, 60, ['flour', 12 , 'milk', 'chocolate'], 'dessert')
#recipe5 = Recipe('Cake', 5, 60, 'd', 'dessert')
#recipe5 = Recipe('Cake', 5, 60, -3, 'dessert')

#recipe5 = Recipe('Paella', 4, 45, ['rice', 'tomatoes', 'squid', 'peper'], 'dinner', 'Delicious typical Spanish lunch')
#recipe5 = Recipe('Paella', 4, 45, ['rice', 'tomatoes', 'squid', 'peper'], 3, 'Delicious typical Spanish lunch')


my_book = Book('my_book')

#my_book2 = Book('')
#my_book3 = Book(1)


my_book.add_recipe(recipe1)
my_book.add_recipe(recipe2)
my_book.add_recipe(recipe3)
sleep(2)
my_book.add_recipe(recipe4)

fake_recipe = "fake"
#my_book.add_recipe(fake_recipe)

my_book.get_recipes_by_types("starter")
my_book.get_recipes_by_types("lunch")
my_book.get_recipes_by_types("dessert")

#my_book.get_recipes_by_types("dinner")

print(my_book.creation_date)
print(my_book.last_update)
#print(dir(my_book))

my_recipe1 = my_book.get_recipe_by_name("SALAD")
my_recipe2 = my_book.get_recipe_by_name("PaElla")
print(str(my_recipe2))

my_recipe3 = my_book.get_recipe_by_name("pasta")
print(str(my_recipe3))



import unittest

from recipe import Recipe

class TestRecipe(unittest.TestCase):
    
    def test_typeerror_1(self):
        with self.assertRaises(TypeError):
            recipe = Recipe('Paella', 4, 45, ['rice', 'tomatoes', 'squid', 'peper'], 'lunch', 'Delicious typical Spanish lunch')
            
    def test_typeerror_2(self):
        with self.assertRaises(TypeError):
            is_prime('five')
    def test_valueerror(self):
        with self.assertRaises(ValueError):
            is_prime(-4)


class TestBook(unittest.TestCase):
    
    def test_typeerror_1(self):
        with self.assertRaises(TypeError):
            is_prime(6.5)
    def test_typeerror_2(self):
        with self.assertRaises(TypeError):
            is_prime('five')
    def test_valueerror(self):
        with self.assertRaises(ValueError):
            is_prime(-4)

            
if __name__=='__main__':
	unittest.main()