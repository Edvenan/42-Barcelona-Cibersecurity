from recipe import Recipe
from datetime import datetime

class Book:
    
    def __init__(self, name):
        name: str
        
        # name initilizattion
        assert isinstance(name, str), f"Invalid Data type. The 'recipe name' must be a string."
        assert name != "", f"Missing Data. A 'recipe name' must be provided at object creation."
        self.name = name.lower()                   

        # other attributes initialization
        self.last_update = datetime.now()
        self.creation_date = datetime.now()
        self.recipes_list = {"starter":[], "lunch":[], "dessert":[]}
        
    def get_recipe_by_name(self,name: str):
        """Prints a recipe with the name \texttt{name} and returns the instance"""
        
        assert isinstance(name, str), f"Invalid Data type. The 'recipe name' must be a string."
        assert name != "", f"Missing Data. A 'recipe name' must be provided."
        # local vars
        result = None
        
        for group in self.recipes_list.values():
            for recipe in group:
                if recipe.name == name.lower():
                    print(str(recipe))
                    result = recipe
        if not result:
            print(f"Data not found. There is no recipe in this book called '{name}'.")
        return result
    
    def get_recipes_by_types(self,recipe_type: str):
        """Get all recipe names for a given recipe_type"""

        assert isinstance(recipe_type, str), f"Invalid Data type. The 'recipe type' must be a string."
        assert recipe_type != "", f"Missing Data. A 'recipe type' must be provided."
        assert recipe_type.lower() in self.recipes_list.keys(), f"Invalid Data. Book does not accept '{recipe_type}' recipes. Only 'starter', 'lunch' and 'dessert'"

        if len(self.recipes_list[recipe_type]) == 0:
            print(f"Data not found. There are no '{recipe_type}' recipes in this Book")
        else:
            print(f"List of {recipe_type} recipes:")
            print(*["  - "+recipe.name for recipe in self.recipes_list[recipe_type]], sep="\n")
            print("")

                
    def add_recipe(self,recipe: Recipe):
        """Add a recipe to the book and update last_update"""
        assert isinstance(recipe, Recipe), f"Invalid Data type. The '{recipe}' object provided is not a recipe."
        # Add the recipe to the recipes_list
        self.recipes_list[recipe.recipe_type].append(recipe)
        self.last_update = datetime.now()
