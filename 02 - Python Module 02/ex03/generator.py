#!/usr/bin/env python

"""
Code a function called generator that takes a text as input (only printable
characters), uses the string parameter sep as a splitting parameter, and 
yields the resulting substrings.
The function can take an optional argument. 
The options are:
• shuffle: shuffles the list of words,
• unique: returns a list where each word appears only once,
• ordered: alphabetically sorts the words. 
"""

import random

# using Fisher–Yates shuffle Algorithm
def FisherYates_shuffle(words):
    # to shuffle a list
    for i in range(len(words)-1, 0, -1):
        
        # Pick a random index from 0 to i
        j = random.randint(0, i + 1)
    
        # Swap word[i] with the element at random index
        words[i], words[j] = words[j], words[i]
        return words

def generator(text: str, sep:str=" ", option:str=None):
    '''Splits the text according to sep value and yield the substrings.
    option precise if a action is performed to the substrings before it is yielded.
    '''
    # Text type error handling
    if not isinstance(text, str):
        print("ERROR")
        exit(1)
    
    # Generate list of words from text        
    words = text.split(sep)

    # Manipulate list of words if valid option
    if option:
        if not isinstance(option,str):
            # Option type error handling
            print("ERROR")
            exit(1)
        
        elif option.lower() == 'shuffle':
            FisherYates_shuffle(words)
        
        elif option.lower() == 'unique':
            words = list(dict.fromkeys(words))

        elif option.lower() == 'ordered':
            words.sort(key=str.lower)
        else:
            # Option value error handling
            print("ERROR")
            exit(1)
    
    # Yield each word in word list            
    for word in words:
        yield word


# TESTS
'''
text = "Le Lorem Ipsum est simplement du faux texte."

for word in generator(text, sep=" "):
    print(word)
    
print("")

for word in generator(text, sep=" ", option="shuffle"):
    print(word)

print("")

for word in generator(text, sep=" ", option="ordered"):
    print(word)
    
print("")
    
text = "Lorem Ipsum Lorem Ipsum"

for word in generator(text, sep=" ", option="unique"):
    print(word)

print("")

text = "Lorem/Ipsum/Lorem/Ipsum"

for word in generator(text, sep=" ", option=4):
    print(word)

print("")

text = 1.0
for word in generator(text, sep="."):
    print(word)
'''