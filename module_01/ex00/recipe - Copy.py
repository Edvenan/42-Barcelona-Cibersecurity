
class Recipe:
    def __init__(self, name, cooking_lvl, cooking_time, ingredients, recipe_type, description=''):
        name: str
        cooking_lvl: int
        cooking_time: int
        ingredients: list[str]
        recipe_type: str
        description: str
        
        # name initilizattion
        if isinstance(name, str):
            if name == "":
                print(f"Missing Data. A 'recipe name' must be provided at object creation.")
                return None
            else:
                self.name = name.lower()                    
        else:
            print(f"Invalid Data type. The 'recipe name' must be a string.")
            return None
            
        # cooking_lvl initilizattion
        if isinstance(cooking_lvl, int):
            if cooking_lvl in range(1,6):
                self.cooking_lvl = cooking_lvl              
            else:
                print(f"Invalid Data. The 'cooking level' must be between 1 and 5.")
                return None               
        else:
            if cooking_lvl == "":
                print(f"Missing Data. A 'cooking level' must be provided at object creation.")
            else:
                print(f"Invalid Data type. The 'cooking level' must be an integer.")
            return None
            
        # cooking_time initilizattion
        if isinstance(cooking_time, int):
            if cooking_time >= 0:
                self.cooking_time = cooking_time    
            else:
                print(f"Invalid Data. The 'cooking time' must be higher or equal to zero.")
                return None                    
        else:
            if cooking_time == "":
                print(f"Missing Data. A 'cooking time' must be provided at object creation.")
            else:
                print(f"Invalid Data type. The 'cooking time' must be an integer higher or equal to zero.")
            return None
        
        # ingredients initilizattion
        if isinstance(ingredients, list):
            if len(ingredients) > 0:
                # Check if all ingredients in list are valid strings
                valid_list = True
                for ing in ingredients:
                    if not isinstance(ing, str):
                        print(f"Invalid Data type. All 'ingredients' must be strings.")
                        valid_list = False
                if valid_list:
                    self.ingredients = ingredients
                else:
                    return None
            else:
                print(f"Missing Data. 'Ingredients' must be provided at object creation.")                    
                return None
        else:
            print(f"Invalid Data type. 'Ingredients' must be a list of strings.")
            return None
        
        # recipe_type initilizattion
        if isinstance(recipe_type, str):
            if recipe_type == "":
                print(f"Missing Data. A 'recipe type' must be provided at object creation.")
                return None
            else:
                if recipe_type.lower() in ["starter", "lunch", "dessert"]:
                    self.recipe_type = recipe_type.lower()
                else:
                    print(f"Invalid Data. The 'recipe type' must be a choice of: 'starter', 'lunch' or 'dessert'.")
                    return None                     
        else:
            print(f"Invalid Data type. The 'recipe type' must be a string'.")
            raise ValueError(f"Invalid Data type. The 'recipe type' must be a string'.")
        
        
        # description initilizattion
        if isinstance(description, str):
            self.description = description
        else:
            print(f"Invalid Data type. The 'recipe description' must be a string.")
            return None
        

    
    def __str__(self):
        """Return the string to print with the recipe info"""
        
        text1 = f"\nRecipe Name: {self.name}\n"
        text2 = f"   Cooking Level: {self.cooking_lvl}\n"
        text3 = f"   Cooking Time:  {self.cooking_time}\n"
        text4 = f"   Ingredients:   {self.ingredients}\n"
        text5 = f"   Recipe Type:   {self.recipe_type}\n"
        text6 = f"   Description:   {self.description}\n"

        text = text1+text2+text3+text4+text5+text6
        return text