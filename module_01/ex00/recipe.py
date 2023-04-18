
class Recipe:
    def __init__(self, name, cooking_lvl, cooking_time, ingredients, recipe_type, description=''):
        name: str
        cooking_lvl: int
        cooking_time: int
        ingredients: list[str]
        recipe_type: str
        description: str
        
        # Name error handling
        if not isinstance(name, str):
            raise TypeError(f"The 'recipe name' must be a string.")
        if name == "":
            raise ValueError(f"A 'recipe name' must be provided at object creation.")
        # Name initilizattion
        self.name = name.lower()                    
            
        # cooking_lvl error handling
        if not isinstance(cooking_lvl, int):
            raise TypeError(f"The 'cooking level' must be an integer.")
        if cooking_lvl == "":
            raise ValueError(f"A 'cooking level' must be provided at object creation.")
        if not cooking_lvl in range(1,6):
            raise ValueError(f"The 'cooking level' must be between 1 and 5.")
        # cooking_lvl initilizattion
        self.cooking_lvl = cooking_lvl              
            
        # cooking_time error handling
        if not isinstance(cooking_time, int):
            raise TypeError(f"The 'cooking time' must be an integer.")
        if cooking_time == "":
            raise ValueError(f"A 'cooking time' must be provided at object creation.")
        if cooking_time < 0:
            raise ValueError(f"The 'cooking time' must be higher or equal to zero.")
        # cooking_time initilizattion
        self.cooking_time = cooking_time    
        
        # ingredients initilizattion
        assert isinstance(ingredients, list), f"Invalid Data type. 'Ingredients' must be a list of strings."
        assert len(ingredients) > 0, f"Missing Data. 'Ingredients' must be provided at object creation."
        # Check if all ingredients in list are valid strings
        for ing in ingredients:
            assert isinstance(ing, str), f"Invalid Data type. All 'ingredients' must be strings."
        self.ingredients = ingredients

        # recipe_type initilizattion
        assert isinstance(recipe_type, str), f"Invalid Data type. The 'recipe type' must be a string'."
        assert recipe_type != "", f"Missing Data. A 'recipe type' must be provided at object creation."
        assert recipe_type.lower() in ["starter", "lunch", "dessert"], f"Invalid Data. The 'recipe type' must be a choice of: 'starter', 'lunch' or 'dessert'."
        self.recipe_type = recipe_type.lower()
        
        # description initilizattion
        assert isinstance(description, str), f"Invalid Data type. The 'recipe description' must be a string."
        self.description = description

    
    def __str__(self):
        """When you find in the code 'print(reicpe)' this function will return the
           following string with the recipe info"""
        
        text1 = f"\nRecipe Name: {self.name}\n"
        text2 = f"   Cooking Level: {self.cooking_lvl}\n"
        text3 = f"   Cooking Time:  {self.cooking_time}\n"
        text4 = f"   Ingredients:   {self.ingredients}\n"
        text5 = f"   Recipe Type:   {self.recipe_type}\n"
        text6 = f"   Description:   {self.description}\n"

        text = text1+text2+text3+text4+text5+text6
        return text