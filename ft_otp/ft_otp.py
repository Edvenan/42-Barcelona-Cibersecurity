#!/usr/bin python3

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


# TOPT( hex clave inicial) -> ephimeral 6 char password

# HMAC - hash-based message autentication code. Needs (1) hash function and 
#       (2) a symmetric secret key

# https://www.thesecuritybuddy.com/cryptography-and-python/how-to-use-hmac-in-python/


# X represents the time step in seconds (default value X = 30 seconds) and is a 
# system parameter.

# T0 is the Unix time to start counting time steps (default value is 0, 
# i.e., the Unix epoch) and is also a system parameter.

# TOTP = HOTP(K, T), where T is an integer and represents the number of time
# steps between the initial counter time T0 and the current Unix time.
# T = (Current Unix time - T0) / X
# For example, with T0 = 0 and Time Step X = 30, T = 1 if the current Unix time
# is 59 seconds, and T = 2 if the current Unix time is 60 seconds.
# this algorithm MUST support a time value T larger than a 32-bit integer

# keys SHOULD be chosen at random or using a cryptographically strong pseudorandom
# generator properly seeded with a random value.

# Keys SHOULD be of the length of the HMAC output to facilitate interoperability.

# We also RECOMMEND storing the keys securely in the validation system, and, 
# more specifically, encrypting them

# We RECOMMEND a default time-step size of 30 seconds.  This default value of 30
# seconds is selected as a balance between security and usability.

# openssl rand -hex 32 | tr -d "\n" > key.hex
# xxd -p key.txt | tr -d "\n" > key.hex

# echo -n "Esta es mi clave personal 12345" > key.txt
# xxd -p key.txt > key.hex & cat key.hex|wc -c 

# https://www.youtube.com/watch?v=VOYxF12K1vE
# https://totp.app/

'''
      * This method uses the JCE to provide the crypto algorithm.
      * HMAC computes a Hashed Message Authentication Code with the
      * crypto hash algorithm as a parameter.
      *
      * @param crypto: the crypto algorithm (HmacSHA1, HmacSHA256,
      *                             HmacSHA512)
      * @param keyBytes: the bytes to use for the HMAC key
      * @param text: the message or text to be authenticated
      */
'''      

import hashlib
import hmac

key = "Secret Key"
message = "Secret Message"
h = hmac.new(key.encode(), message.encode(), hashlib.sha512).hexdigest()

print(h)



 
/**
      * This method converts a HEX string to Byte[]
      *
      * @param hex: the HEX string
      *
      * @return: a byte array
      */
      
 
 


/**
      * This method generates a TOTP value for the given
      * set of parameters.
      *
      * @param key: the shared secret, HEX encoded
      * @param time: a value that reflects a time
      * @param returnDigits: number of digits to return
      * @param crypto: the crypto function to use
      *
      * @return: a numeric String in base 10 that includes
      *              {@link truncationDigits} digits
      */



