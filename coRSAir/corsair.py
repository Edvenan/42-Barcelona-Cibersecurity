#######################################################################################
###  OpenSSL commands
#######################################################################################
###
###  https://geekflare.com/openssl-commands-certificates/
###
#######################################################################################
###  PUBLIC & PRIVATE KEY GENERATION, DOCUMENT SIGNATURE AND SIGNATURE VERIFICATION
#######################################################################################
### Generate a 2048-bit long private RSA key
###
### > openssl genrsa -out my_private_key.pem 2048 (/4096)      (in addition we can use a pass phrase for the private key => "openssl genrsa -aes256 -out my_private_key 4096")
###
### Obtain the corresponding public key from previous private key
###
### > openssl rsa -in my_private_key.pem -outform PEM -pubout -out my_public_key.pem     
###
### Let's sign a document (test.txt) using the public key
###
### > openssl sha1 -sign my_private_key.pem test.txt > sig.bin (signature file)
###
### Lt's verify the signatture of the document
###
### > openssl sha1 -verify my_public.key.pem -signature sig.bin test.txt
####################################################################################
### Dump the content of the private key and public key:
###
### > openssl rsa -text -in my_private_key.pem
###
####################################################################################
### Encrypt/Decrypt a file using public / private key
####################################################################################
###
### > openssl rsautl -encrypt -in demo.txt -pubin -inkey my_public_key.pem -out demo_encrypt.txt
###
### See encrypted file content:
###
### > xxd demo_encrypt.txt
###
### Let's decrypt using private key
###
### > openssl rsautl -decrypt -in demo_encrypt.txt -inkey my_private_key.pem -out demo_decrypted.txt
### > cat demo_decrypted.txt
###
#######################################################################################
###   convertir keys a Base64 permite enviar contenido de keys sin riesgo a perder info
#######################################################################################
###
#######################################################################################
###  RSA KEY GENERATION AND ENCRYPTION/DECRYPTION
#######################################################################################
###
###  https://www.youtube.com/watch?v=j2NBya6ADSY&t=1222s
###  Prime: number whose factors are only 1 and itself (i.e. 1, 3, 5, 7, 11...)
###  Semi-prime: number whose factors are prime numbers (i.e. 21 => 1, 3, 7, 21)
###  The product of 2 primes is always a semi-prime number
###  Modulo = remainder   (i.e. 13 MOD 5 = remainder of 13/5 = 3)
###
###  step 1) p·q = N    (p, q prime factors of N) (N is a semi-prime)
###  step 2) (p-1)·(q-1) = T (Totient)  =>   e·d = T    =>  find e.d such as e.d mod T = 1
###  step 3) select Public Key: (E)   => a) must be co-prime with N and T  b) must be less that T  c) must NOT be factor of T
###  step 4) select Private Key: (D)   => a) (E·D) MOD T = 1
###
### Encryption:   (msg)^E MOD N = Chiper text
### Encryption:   (msg)^D MOD N = dechiper text
###
### RSA is commutative (keys are commutative): we can encrypt with private key and decrypt with public key
###
### Two numbers are called relatively prime, or coprime, if their greatest common divisor equals 1.[14] For example, 9 and 28 are coprime.

# A partir de dos o más certificados verificar si son vulnerables y en caso afirmativo generar claves privadas capaces de descifrar los mensajes firmados con ellos.
#
# > Podéis generar una herramienta única y autónoma o desarrollar un programa con un conjunto de herramientas que permitan realizar la tarea.

#> Qué elementos componen un certificado digital? -> exponente clave publica (e)  y el modulus (n)
#> Qué elementos componen una clave pub/priv RSA?    

# PEM (Privacy-Enhanced Mail) format is a text-based format for representing cryptographic objects such as keys and certificates. 
# It uses ASCII characters to represent binary data. However, binary data may contain characters that are not valid or may be interpreted 
# differently in certain text-based systems. Base64 encoding converts binary data into a set of ASCII characters that can be safely represented 
# and transmitted in text-based formats.
# PEM KEY -> DER-encoded data (ascii chars representing binary data) is then base64 encoded (to binary)


# 1) Obtener clave pública a partir de un certificado. 
# 2) Obtener módulo y exponente a partir de la clave pública.
# 3) Comparar módulos y obtener el m.c.d. (Algoritmo de Euclides).
#    (21,15) => (6,15) => (6,9) => (6,3) => (3,3) => (0,3) => m.c.d = 3
# 4) partir de p y q generar la clave privada.
# 5) Descifrar el mensaje. 
#
#
#  BigNumber: division rusa
#

import rsa          # https://stuvel.eu/python-rsa-doc/


###  GENERATE RSA PRIV & PUB KEYS
public_key, private_key = rsa.newkeys(1024)

print("\nGenerated Public Key:\n====================\n",public_key)
print("\nGenerated Private Key:\n====================\n",private_key)

### STORE KEYS
with open('public.pem', 'wb') as f:
    f.write(public_key.save_pkcs1("PEM"))
    
with open('private.pem', 'wb') as f:
    f.write(private_key.save_pkcs1("PEM"))


### OPEN/ READ KEYS
with open('public.pem', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
    
with open('private.pem', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())
    

#### ENCRYPTING MESSAGE USING PUB_KEY
message = "This is my secret message to you!"

encrypted_msg = rsa.encrypt(message.encode(), public_key)

with open("encrypted_msg.txt", 'wb') as f:
    f.write(encrypted_msg)

#### DECRYPTING MSG
# open encrypted msg
encrypted_msg = open("encrypted_msg.txt", 'rb').read()
# decrypt
decrypted_msg = rsa.decrypt(encrypted_msg, private_key)

print(decrypted_msg.decode())    # original plain text msg


### SIGNING MSGS

message = "I am telling you that I owe you 10 bucks"

signature = rsa.sign(message.encode(), private_key, "SHA-256")

# writing msg signature to file
with open("signature.txt", 'wb') as f:
    f.write(signature)

# reading signed msg from File
with open("signature.txt", 'rb') as f:
    signature = f.read()

# now verify if read signature is related to the msg
print( rsa.verify(message.encode(), signature, public_key) )     # -> returns 'SHA-256' which means it is verified correctly. Else, it raises a VerificationError("Verification failed")






from math import sqrt


def is_prime(n):
    # this flag maintains status whether the n is prime or not
    prime_flag = 0
    
    if(n > 1):
        for i in range(2, int(sqrt(n)) + 1):
            if (n % i == 0):
                prime_flag = 1
                break
        if (prime_flag == 0):
            print("True")
        else:
            print("False")
    else:
        print("False")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a = 12345678901234567890
b = 9876543210987654321

'''
print(gcd(a,b))

gcd = 90000000009

print(a/gcd)
print(b/gcd)
is_prime(gcd)
is_prime(a/gcd)
is_prime(b/gcd)
'''



# If we have information about two different RSA certificates and suspect that they share one prime factor (either p or q) due 
# to a low entropy random number generator (RNG) used during their generation, it is possible to exploit this vulnerability to 
# try to figure out the private keys.

# To proceed with this attack, we can follow a method known as the Common Factor Attack or Common Modulus Attack. 
# Here's a high-level outline of the steps involved:

# 1) Obtain the modulus (N) and public exponent (e) for both RSA certificates.

# 2) Compare the modulus values. If the modulus are the same, it indicates that at least one prime factor is shared between the two certificates.

# 3) Calculate the greatest common divisor (GCD) of the two modulus. If the GCD is greater than 1, it means that a common prime factor has been found.

# 4) Calculate the greatest common divisor (GCD) of the two moduli using an algorithm like Euclidean algorithm. If the GCD is greater than 1, it indicates 
# the presence of a common prime factor shared between the two certificates. Let's assume that the GCD is equal to the common prime factor, which we'll denote as 'p'. 
# To determine the private keys, we need to calculate the other prime factor, 'q'. Since 'N' is the product of two primes, we can use the formula N = p * q to find
# 'q' by dividing 'N' by 'p'.
# Once we have both prime factors, 'p' and 'q', we can calculate the private keys (d) using the extended Euclidean algorithm or any relevant mathematical technique.
# 4) Once the common factor is determined, compute the private keys (d) using the extended Euclidean algorithm or any relevant mathematical technique.

# 5) With the knowledge of the private key, you can decrypt encrypted messages or perform other operations that require the private key.

'''
It's important to note that successfully carrying out this attack depends on various factors, including the strength of the common factor, the size of the modulus, and the specifics of the RSA implementation. In practice, this attack is typically mitigated by using secure RNGs and proper key generation techniques.

It's essential to remember that attempting to exploit such vulnerabilities in real-world scenarios is illegal and unethical unless explicitly authorized and conducted for legitimate security assessment purposes.


As an AI language model, I can provide information about various types of random number generators (RNGs), including those with low entropy. However, it's important to note that using RNGs with low entropy can compromise the randomness and security of generated numbers. It is generally recommended to use RNGs with high entropy for cryptographic purposes.

That being said, there are several examples of RNGs with low entropy:

Linear Congruential Generator (LCG): LCGs are simple and computationally efficient RNGs. However, they can have low entropy and exhibit predictable patterns if not properly seeded or if the parameters are poorly chosen.

Middle Square Method: The Middle Square Method is a simple RNG that squares a seed value and extracts a portion of the resulting middle digits as the next pseudo-random number. This method is susceptible to low entropy and does not produce high-quality random numbers.

RANDU: RANDU is an infamous RNG that was widely used in the past. It is a linear congruential generator with particularly poor statistical properties and low entropy. It is not suitable for cryptographic purposes.

These examples highlight RNGs that are known for their low entropy and inadequate random properties. They should be avoided in applications that require secure random number generation.

For cryptographic purposes or applications requiring high-quality randomness, it is recommended to use well-vetted and properly seeded RNGs, such as cryptographic RNGs (CSPRNGs) or hardware random number generators (HRNGs), which aim to provide high entropy and strong randomness.
'''