#!/usr/bin python3

# Time-based One Time Password
# ------------------------------
# En el lenguaje de tu elección, debes implementar un programa que permita registrar
# una clave inicial, y sea capaz de generar una nueva contraseña cada vez que se 
# solicite.
# Puedes utilizar cualquier librería que facilite la implementación del algoritmo, 
# siempre que no hagan el trabajo sucio, es decir, queda terminantemente prohibido 
# hacer uso de cualquier librería TOTP. Por supuesto, puedes y debes hacer uso de 
# alguna librería o función que te permita acceder al tiempo del sistema.
# Un ejemplo del uso del programa sería:
#   •El programa deberá llamarse ft_otp.
#   •Con la opción -g , el programa recibirá como argumento una clave hexadecimal
#    de al menos 64 caracteres. 
#   •El programa guardará a buen recaudo esta clave en un archivo llamado ft_otp.key,
#    que estará cifrado en todo momento.
#   •Con la opción -k, el programa generará una nueva contraseña temporal y la mos-
#    trará en la salida estándar.


import argparse
import hmac
import hashlib
import string
# pycryptodome
from Crypto.Cipher import AES
import secrets
import time
import urllib.parse
import base64
import qrcode
import sys
import subprocess
import traceback

###########################
# TOTP generator
###########################
def generateTOTP(key, returnDigits, crypto):
      codeDigits = int(returnDigits)
      result = None
      # Define T0
      T0 = 0
      # calculate steps until now   
      X = 30                          # time step
      timeNow = int(time.time())      # time now
      steps = "0"
      # floor division
      T = (timeNow -T0)// X                # num of time steps until now (int)

      # convert T to a zero-padded hexadecimal string with a width of 16 characters
      steps = format(T, '016X')

      # zerofill steps (str) if needed
      while len(steps) < 16:
            steps = "0" + steps         

      # convert HEX string to Byte
      msg = bytes.fromhex(steps)
      k = bytes.fromhex(key)

      hash = hmac.new(k, msg, hashlib.__dict__[crypto]).digest()

      # put selected bytes into result int
      offset = hash[-1] & 0xf
 
      # apply binary operations to 4 bytes from offset (int)
      binary = ((hash[offset] & 0x7f) << 24) | \
                  ((hash[offset + 1] & 0xff) << 16) | \
                  ((hash[offset + 2] & 0xff) << 8) | \
                  (hash[offset + 3] & 0xff)

      otp = binary % 10**codeDigits

      # convert TOTP from int to str
      result = str(otp)
      
      # if the generated otp has less digits than the returnDigit parameter
      # we zerofill it to match it
      while len(result) < codeDigits:
            result = "0" + result
      return result

###########################
# Get hex message from file
###########################
def get_hex_msg_from_file(input_file):

      try:      
            with open(input_file, 'r') as f:
                  hex_message = f.read().strip()
            
            return hex_message
      
      except:
            # obtain/print exception info & return Cntxt Mgr object
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback)
            print(f"{exc_type.__name__}: {exc_value}")
            exit(2)
      
###########################
# convert text to hex
###########################
def string2hex(message):
      # Convert plain text message into hexadecimal
      # Convert the text to bytes
      encoded = message.encode('utf-8')
      # Convert the bytes to a hexadecimal string
      hex_message = encoded.hex()
      return hex_message

###########################
# convert hex to text
###########################
def hex2string(hex_message):
      # Convert the decrypted hex message back into plain text
      message = bytes.fromhex(hex_message).decode('utf_8')
      return message
    
###########################
# encrypt hex msg into file
###########################
def encrypt_and_save_hex_message(hex_message, output_filename, password=b'This is my secret encryption key'):

      # Encrypt the hex message using AES and a given password

      # we use the AES EAX Mode that provides confidentiality and integrity.
      # generate a cipher
      cipher = AES.new(password, AES.MODE_EAX)
      # encrypt the message and generate a tag for integrity verification purposes
      ciphertext, tag = cipher.encrypt_and_digest(bytes.fromhex(hex_message))

      # Store the encrypted message into the output file
      # we write the file in binary mode
      with open(output_filename, 'wb') as f:
            [ f.write(x) for x in (cipher.nonce, tag, ciphertext) ]

###########################
# decrypt hex msg from file
###########################
def decrypt_hex_message_from_file(input_filename, password=b'This is my secret encryption key'):
      # Read the encrypted hex message from the input file
      # we read the file in binary mode
      # Nonce (first 16 bytes):, a random value that should be used once per message with a particular key,
      # Tag (next 16bytes): to verify integrity and untampering and
      # Encrypted text or ciphertext (remaining bytes)
      try:
            with open(input_filename, 'rb') as f:
                  nonce, tag, ciphertext = [ f.read(x) for x in (16, 16, -1) ]

            # Decrypt the hex message using AES and a given key

            # replicate the cipher used during encryption using the nonce read from file
            cipher = AES.new(password, AES.MODE_EAX, nonce=nonce)
            # decrypt the message and verify integrity
            try:
                  hex_message = cipher.decrypt_and_verify(ciphertext, tag)
                  return hex_message.hex()
            except ValueError:
                  return None
      except:
            # obtain/print exception info & return Cntxt Mgr object
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback)
            print(f"{exc_type.__name__}: {exc_value}")
            exit(2)
            
###########################
# create URI
###########################
def create_URI(issuer_name, user_name, secret_key):

      # Convert the secret key to base32 encoding
      secret_base32 = base64.b32encode(bytes.fromhex(secret_key)).decode('utf-8')

      # Create the URI
      uri = 'otpauth://totp/{label}?secret={secret}&issuer={issuer}'.format(
            label=urllib.parse.quote(user_name),
            secret=secret_base32,
            issuer=urllib.parse.quote(issuer_name)
            )
      return uri

###########################
# generate RQ code
###########################
def create_QR(uri):

      # Qr code generation step
      try:
            qrcode.make(uri).save("qr.png")
      except:
            # obtain/print exception info & exit
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback)
            print(f"{exc_type.__name__}: {exc_value}")
            exit(2)

###########################
# generate random 32-byte key
###########################
def generate_random_key():
      # generating random key
      rand_key = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                  for i in range(32))
      return rand_key

###########################
# format user's passwords
###########################
def format_user_password(password):
      
      # zerofill password (str) if needed
      if len(password) < 16:
            while len(password) < 16:
                  password = "0" + password
      elif len(password) < 24:
            while len(password) < 24:
                  password = "0" + password
      elif len(password) < 32:
            while len(password) < 32:
                  password = "0" + password
      else:
            password = password [:32]
      # convert to Byte
      password = bytes(password, 'utf_8')
      
      return password

###########################
# ask user cipher password
###########################
def ask_user_cipher_password():
      # ask the user if they want to use a password to cipher
      # the shared secret key
      password = str(input("Please enter your password to cipher your Shared Secret Key or press Enter for a default one:\n>> "))
      if password == "":
                  return None
      else:
            # return formated user passwd
            return format_user_password(password)
      
###########################
# ask user decipher password
###########################
def ask_user_decipher_password(trials):
      if trials == 0:
            password = str(input("Please enter your password to decipher your Shared Secret Key (press 'quit' to cancel):\n>> "))
      elif trials <2:
            password = str(input("Wrong password! You have {} attempts left.\nPlease enter your password to decipher your Shared Secret Key (press 'quit' to cancel):\n>> ".format(3-trials)))
      elif trials == 2:
            password = str(input("Wrong password! Last attempt!\nPlease enter your password to decipher your Shared Secret Key (press 'quit' to cancel):\n>> "))
      else:
            print("Max number of attempts reached. Goodbye!")
            exit()
      if password.lower() == 'quit':
            exit()
      
      return format_user_password(password)
            
###########################
# get oathtool TOTP
###########################
def get_oathtool_totp(key, crypto, returnDigits):

      cmd = f"oathtool --totp={crypto} --digits={returnDigits} {key}"
      try:
            result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
            output = result.stdout.decode().strip()
            return output
      except FileNotFoundError:
            # obtain/print exception info & return  
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback)
            #print(f"{exc_type.__name__}: {exc_value}")
            print("OathTool not found. Please install it to obatin a TOTP verification in the app.")
            return "-"*int(returnDigits)

######################################
# MAIN
######################################
def main():
    
      output_filename = "ft_otp.key"
      returnDigits = '6'
      crypto_alg = "sha1"
      
      issuer_name = '42-FT'
      user_name = 'Eduard Vendrell'


      # handle arguments input by user
      parser = argparse.ArgumentParser(description='This is an implementation of the TOTP algorithm by Eduard Vendrell.')
      parser.add_argument('-g', '--hexfile', type=str, help='Path to the hex file')
      parser.add_argument('-k', '--keyfile', type=str, help='Path to the key file')
      parser.add_argument('-p', '--password', type=str, help='Password to cipher secret key')
      args = parser.parse_args()

      if args.hexfile:
            # Do something with the 'key.hex' file

            # obtain hex message from input file
            hex_message = get_hex_msg_from_file(args.hexfile)
                       
            # we store the shared secret key (in HEX) because
            # we will use it to provision a URI (Uniform Resource Identifier)
            # with the name of the user and the issuer.
            secret_key = hex_message
            uri = create_URI(issuer_name, user_name, secret_key)

            # ask the user if they want to use a password to cipher
            # the shared secret key
            password = ask_user_cipher_password()
            
            if password:
                  # encrypt hex message and store it into 'ft_otp.key' file
                  # using user's password
                  encrypt_and_save_hex_message(hex_message, output_filename, password)
            else:
                 # encrypt hex message and store it into 'ft_otp.key' file
                  # using default password
                  encrypt_and_save_hex_message(hex_message, output_filename)
        
        
      elif args.keyfile:
            # Do something with the 'ft_otp.key' file
            
            # obtain shared secret key from file
            key_hex = decrypt_hex_message_from_file(args.keyfile)
            
            # if decipher fails with deafult password (hex_key = None), 
            # it means that the SSK was ciphered using a user password.
            # Ask user for it (he'll have 3 attempts only):
            trials = 0
            while not key_hex:
                  password = ask_user_decipher_password(trials)
                  key_hex = decrypt_hex_message_from_file(args.keyfile, password)
                  trials += 1
                  
            # we store the shared secret key (in HEX) to 
            # provision a URI (Uniform Resource Identifier)
            # with the name of the user and the issuer.
            secret_key = key_hex
            uri = create_URI(issuer_name, user_name, secret_key)
            create_QR(uri)
            
            # generate TOTP
            otp = generateTOTP(key_hex, returnDigits, crypto_alg)
            
            print(otp)
            print("OathTool's TOTP: {}".format(get_oathtool_totp(key_hex, 'sha1','6')))

      elif args.password:
            # Do something with the password to cipher the sahared secret key
            pass
      
      else:
            # No file specified
            print("Please specify a file")

if __name__ == '__main__':
    main()
        