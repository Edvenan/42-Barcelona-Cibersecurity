from recipe import Recipe
from datetime import datetime

class Book:
    
    def __init__(self, name):
        name: str
        
        self.name = name.lower()                # (str):nameofthebook, 
        self.last_update = datetime.now()       # (datetime):thedateofthelastupdate
        self.creation_date = datetime.now()      # (datetime):thecreationdate
        self.recipes_list = {"starter":[], "lunch":[], "dessert":[]}        # (dict):adictionnarywith3keys:"starter","lunch","dessert".
        
    def get_recipe_by_name(self,name: str):
        """Prints a recipe with the name \texttt{name} and returns the instance"""
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
        #...Yourcodehere... 

        if recipe_type.lower() in self.recipes_list.keys():
            if len(self.recipes_list[recipe_type]) == 0:
                print(f"Data not found. There are no '{recipe_type}' recipes in this Book")
                return None
            else:
                print(f"List of {recipe_type} recipes:")
                print(*["  - "+recipe.name for recipe in self.recipes_list[recipe_type]], sep="\n")
                print("")
        else:
            print(f"Invalid Data. Book does not accept '{recipe_type}' recipes. Only 'starter', 'lunch' and 'dessert'")
            return None
            
    
    def add_recipe(self,recipe):
        recipe: Recipe
        """Add a recipe to the book and update last_update"""
        #...Your code here...handle error if arg is not a Recipe

        if isinstance(recipe, Recipe):
            # Add the recipe to the recipes_list
            self.recipes_list[recipe.recipe_type].append(recipe)
            self.last_update = datetime.now()
        else:
            print(f"Invalid Data type. The '{recipe}' object provided is not a recipe.")
            return None