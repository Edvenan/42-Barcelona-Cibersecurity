from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import os
import sys
import traceback
from gen_private_key import *


####################################################
# EXTRACT EXPONENT & MODULUS FROM ALL PEM FILES 
####################################################

files = []

with os.scandir('./challenge_corsair/') as entries:
    for entry in entries:
        # if file has .pem extension, we add it to the 'files' list.
        if entry.name.split(sep=".")[-1] == "pem":
            files.append(entry.path)


pubkey_data = {}

for file in files:

    # Read the contents of the public_key.pem file
    with open(file, "rb") as key_file:
        pem_data = key_file.read()
        
    # Load the PEM-encoded public key
    try:
        public_key = serialization.load_pem_public_key(pem_data)

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
        print("Public Key reading failed! Affected File : ", file)
        print("-----------------------------------------")
        exit(2)


####################################################
# FIND PRIVATE KEY AND DECRYPT A FILE
####################################################

for file_a, data_a in pubkey_data.items():
    for file_b, data_b in pubkey_data.items():
        if file_a != file_b:

            res_gcd = gcd(data_a[1], data_b[1])
            if res_gcd > 1:
                # There is a common divisor so both modulus are not co-prime
                #print("We got a GCD!\n\tFile1: {}\n\tFile2: {}\n\tGCD ({}): {}".format(file_a, file_b, len(str(res_gcd)),res_gcd))
                p = res_gcd         # int required
                
                # check if p is prime
                """ if is_prime(p):
                    print("\t'p' is prime")
                else: print("\t'p' is NOT prime") """
                    
                q = data_a[1]//p    # int required
                e = data_a[0]
                
                #print("\tPotential 'q' ({}): {}\n".format(len(str(res_gcd)),q))

                # file_name where to store generated private_key
                output_file = f"private_{file_a}"
                
                # Generate PEM+PKCS#8 Private key with the obtained parameters
                pkcs8_private_key = recover_key(p, q, e, output_file)

                # Load the PEM-encoded private key
                # reads the PEM-encoded private key data, performs the necessary parsing, and constructs a private key object that can be used
                # for cryptographic operations. The resulting private_key object is an instance of the 
                # cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey class (assuming an RSA private key).
                private_key = serialization.load_pem_private_key(pkcs8_private_key.encode(), None)

                ###########################################
                ###### GEN PUB KEY FROM CREATED PRIV KEY
                ###########################################                
                # Generate the public key from the generated private key
                public_key = private_key.public_key()

                # Serialize the public key
                public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                #print("GEN PUBLIC KEY: ",public_key_pem.decode('ascii'))
               
               
                ###########################################                
                # Get ORIGINAL public key in PEM format
                ###########################################
                # Load the PEM-encoded public key
                with open(file_a, "rb") as key_file:
                    pem_data = key_file.read()
                orig_public_key = serialization.load_pem_public_key(pem_data)
                #print("ORIGINAL PUBLIC KEY: File {} : {}".format(file_a, pem_data.decode('ascii')))                    
                
                ########################################### 
                # LOAD ENCRYPTED DATA FROM FILE
                ########################################### 
                with open(file_a.replace(".pem", ".bin"), 'rb') as f:
                    encrypted_data = f.read()
                print("Encrypted file: ",file_a.replace(".pem", ".bin"))   
                #############################################################
                # COMPARE GENERATED PUBLIC KEY TO ORIGINAL PUBLIC KEY
                #############################################################
                print("-------------------------------------------------")
                if  pem_data.decode('ascii') == public_key_pem.decode('ascii'):
                    print("GENERATED PUB KEY == ORIGINAL PUB KEY")
                else:
                    print("GENERATED PUB KEY NOT EQUAL TO ORIGINAL PUB KEY")
                print("-------------------------------------------------")

                
                ###################################################################################                
                # DECRYPT MESSAGE USING GENERATD PRIVATE KEY
                ###################################################################################                
                try:    
                    decrypted_data = private_key.decrypt(encrypted_data, padding.PKCS1v15())
                    print("----------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------------")
                    print("Decrypted message: ", decrypted_data.decode())
                    print("----------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------------")
                except:
                    # obtain/print exception info
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    #traceback.print_tb(exc_traceback)
                    print("---------------------------------------------------------------")
                    print("Decryption failed: "+f"{exc_type.__name__}: {exc_value}")
                    print("Affected File : ", file_a)
                    print("==============================================================")
        else:
            continue