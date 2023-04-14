#!/usr/bin/env python

# Python program that takes one string as arguments and encode it into Morse code


import sys

# Dictionary representing the morse code chart
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ' ': '/'}

# Function to encode the string according to the morse code chart

def encode(message):
    # Store message without spaces
    message_wo_spaces = message.replace(" ","")
    
    # Encode message if message without spaces is alphanumeric. Else, error
    
    if message_wo_spaces.isalnum():
        encoded = ''
        for letter in message:
            # Looks up the dictionary and adds the corresponding morse code
            # along with a space to separate morse codes for different characters
            encoded += MORSE_CODE_DICT[letter] + ' '
    else:
        encoded = "ERROR"
    return encoded

# Main function

def main():
     # Store inout arguments in a list
    arguments = sys.argv
    
    # If arguments are provided, encode. Else, do nothing
    if len(arguments) > 1:
        
        # Combine all arguments except [0] in one string
        message = ' '.join(arguments[1:])
        
        # Call encode function and print result
        result = encode(message.upper())
        print(result)
    else:
        pass

# Executes the main function
if __name__ == '__main__':
    main()