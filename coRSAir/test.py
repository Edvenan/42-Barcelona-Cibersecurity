from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os
import sys
import traceback
import  BigNumber
from gen_private_key import *
import base64


####################################################
# GCD
####################################################
def gcd(a:BigNumber, b:BigNumber):
    while b:
        a, b = b, a % b
    return a


###################################################




# Path to the public_key.pem file
#files =["./sample/public.pem", "./2.pem"]
files = []

with os.scandir('./challenge_corsair/') as entries:
    for entry in entries:
        # if file has .pem extension, we add it to the 'files' list.
        if entry.name.split(sep=".")[-1] == "pem":
            files.append(entry.path)
#print(files)


####################################################
# STORE ALL PEM FILES EXPONENT AND MODULUS IN A DICT
####################################################

pubkey_data = {}

for file in files:

    # Read the contents of the public_key.pem file
    with open(file, "rb") as key_file:
        pem_data = key_file.read()
        
    # Load the PEM-encoded public key
    try:
        public_key = serialization.load_pem_public_key(pem_data, backend=default_backend())

        #print(public_key.public_numbers())
        
        # Extract and store in dict the 'exponent' (E)
        exponent = public_key.public_numbers().e
        pubkey_data[file] = [exponent]
        # Extract and store in dict the modulus (N)
        modulus = public_key.public_numbers().n
        pubkey_data[file].append(modulus)

        # Print the extracted values
        """ print("\n-----------------------------------------")
        print("# File : ", file)
        print("-----------------------------------------")
        print("# Exponent (e):", exponent)
        print("# Modulus (n):", modulus)
        print("-----------------------------------------") """
    except:
        # obtain/print exception info
        exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_tb(exc_traceback)
        print(f"{exc_type.__name__}: {exc_value}")
        print("\n-----------------------------------------")
        print("Affected File : ", file)
        print("-----------------------------------------")
        exit(2)

#print(pubkey_data)


####################################################
# COMPARE ALL MODULUS AND FIND (1) GCD (2) 'q' and PRIVATE KEY
####################################################

for file_a, data_a in pubkey_data.items():
    for file_b, data_b in pubkey_data.items():
        if file_a != file_b:
            res_gcd = gcd(data_a[1], data_b[1])
            if res_gcd > 1:
                print("We got a GCD!\n\tFile1: {}\n\tFile2: {}\n\tGCD ({}): {}\n".format(file_a, file_b, len(str(res_gcd)),res_gcd))
                p = res_gcd
                q = data_a[1]/p
                e = data_a[0]
                print("\tPotential 'q' ({}): {}\n".format(len(str(res_gcd)),q))
                
                print(type(p))
                print(type(q))
                output_file = f"private_{file_a}"
                
                pkcs8_private_key = recover_key(p, q, e, output_file)

                #print(pkcs8_private_key)
                #print(pkcs8_private_key.decode('ascii'))
                
                
                # Load the PEM-encoded private key
                private_key = serialization.load_pem_private_key(pkcs8_private_key, None, backend=default_backend())

                # Load encrypted data
                with open(file_a.replace(".pem", ".bin"), 'rb') as f:
                    encrypted_data = f.read()
                print("Encrypted file: ",file_a.replace(".pem", ".bin"))   
                
                 
                #raw_cipher_data = base64.b64decode(encrypted_data)
                
                #phn = cipher.decrypt(raw_cipher_data, <some default>)
                
                try:    
                    decrypted_data = private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("Decrypted message: ", decrypted_data)
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                    print("-----------------------------------------")
                except:
                    # obtain/print exception info
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    #traceback.print_tb(exc_traceback)
                    print(f"{exc_type.__name__}: {exc_value}")
                    print("\n-----------------------------------------")
                    print("Affected File : ", file_a)
                    print("-----------------------------------------")

        else:
            continue




'''
# Perform operations with the public key, e.g., encryption, verification, etc.
# For example, to encrypt a message using the public key:
encrypted_data = public_key.encrypt(b"Your message", padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))



# Path to the private_key.pem file
private_key_path = "./sample/private.pem"

# Read the contents of the private_key.pem file
with open(private_key_path, "rb") as key_file:
    pem_data = key_file.read()

# Load the PEM-encoded private key
private_key = serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())

# Extract the exponent
exponent = private_key.private_numbers().public_numbers.e

# Extract the prime factors p and q
p = private_key.private_numbers().p
q = private_key.private_numbers().q


# Print the extracted values
print("Exponent (e):", exponent)
print("Prime p:", p)
print("Prime q:", q)
print("Modulus (n):", p*q)


# Convert private key to PEM-encoded string
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Print the private key
print(pem_private_key)
# Perform operations with the private key, e.g., decryption, signing, etc.
# For example, to decrypt a message using the private key:
decrypted_data = private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
'''

def egcd(a, b):
        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
        return gcd, x, y


