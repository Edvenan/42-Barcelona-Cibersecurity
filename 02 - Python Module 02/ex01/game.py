#!/usr/bin/env python

""" Create a GotCharacter class and initialize it with the following attributes:
    • first_name,
    • is_alive (by default is True).
    Pick up a GoT House (e.g., Stark, Lannister...) and create a child class that inherits
    from GotCharacter and define the following attributes:
    • family_name (by default should be the same as the Class)
    • house_words (e.g., the House words for the Stark House is: "Winter is Coming")
    Add two methods to your child class:
    • print_house_words: prints the House words,
    • die: changes the value of is_alive to False. """

class GotCharacter:
    def __init__(self, first_name, is_alive=True):
        first_name: str
        
        # First Name error handling
        if not isinstance(first_name, str):
            raise TypeError(f"The 'first name' must be a string.")
        if first_name == "":
            raise ValueError(f"A 'first name' must be provided at object creation.")
        # first_name initilizattion
        self.first_name = first_name                    
        
         # is_alive error handling
        if not isinstance(is_alive, bool):
            raise TypeError(f"The 'is_alive' parameter is boolean and must be either True or False.")

        # is_alive initilizattion
        self.is_alive = is_alive               

class Stark(GotCharacter):
    """A class representing the Stark family. Or when bad things happen to good people."""
    
    def __init__(self, first_name=None, is_alive=True):
        super().__init__(first_name=first_name, is_alive=is_alive)
        self.family_name = "Stark"
        self.house_words = "Winter is Coming"
    
    def print_house_words(self):
        print(self.house_words)
    
    def die(self):
        self.is_alive = False
        
class Lannister(GotCharacter):
    """A class representing the Lannister family. Or when good things happen to bad people."""
    
    def __init__(self, first_name=None, is_alive=True):
        super().__init__(first_name=first_name, is_alive=is_alive)
        self.family_name = "Lannister"
        self.house_words = "Hear me roar"
    
    def print_house_words(self):
        print(self.house_words)
    
    def die(self):
        self.is_alive = False