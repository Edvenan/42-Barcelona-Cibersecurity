from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
import sys
import traceback
from gen_private_key import *
import difflib


####################################################
# EXTRACT EXPONENT & MODULUS FROM ALL PEM FILES 
####################################################

working_folder = './challenge_corsair/'
working_folder = './keys/'
files = []
decrypted_files_counter = 0
file_counter = 0

with os.scandir(working_folder) as entries:
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
    file_counter += 1
    decrypted = False
    for file_b, data_b in pubkey_data.items():
        if file_a != file_b:

            res_gcd = gcd(data_a[1], data_b[1])
            if res_gcd > 1:
                # There is a common divisor so both modulus are not co-prime
                """ print("==================================================================================")
                print("We got a GCD!\nFile1: {}\nFile2: {}".format(file_a, file_b)) """
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
                
                ###########################################
                # Generate PEM+PKCS#8 Private key with the obtained parameters
                ###########################################
                pkcs8_private_key = recover_key(p, q, e, output_file)

                if not pkcs8_private_key: continue

                # Load the PEM-encoded private key
                # reads the PEM-encoded private key data, performs the necessary parsing, and constructs a private key object that can be used
                # for cryptographic operations. The resulting private_key object is an instance of the 
                # cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey class (assuming an RSA private key).
                private_key = serialization.load_pem_private_key(pkcs8_private_key.encode(), None)

                ###########################################
                ###### GEN PUB KEY FROM CREATED PRIV KEY
                ###########################################                
                # Generate the public key from the generated private key (RSAPublicKey object)
                public_key = private_key.public_key()

                # Serialize the public key (byteS)
                public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                #print("GEN PUBLIC KEY: ",public_key_pem.decode('ascii'))
               
               
                ###########################################                
                # Get ORIGINAL public key in PEM format
                ###########################################
                # Load the PEM-encoded public key (bytes)
                with open(file_a, "rb") as key_file:
                    pem_data = key_file.read()
                
                # Serialize the public key (RSAPublicKey object)
                orig_public_key = serialization.load_pem_public_key(pem_data)
                #print("ORIGINAL PUBLIC KEY: File {} : {}".format(file_a, pem_data.decode('ascii')))                    
                
                ########################################### 
                # LOAD ENCRYPTED DATA FROM FILE
                ########################################### 
                filename = file_a.replace(".pem", ".bin")
                filename = filename.replace("pubkey", "ciphertext")

                with open(filename, 'rb') as f:
                    encrypted_data = f.read()
                #print("Encrypted file: ",filename)   
                #############################################################
                # COMPARE GENERATED PUBLIC KEY TO ORIGINAL PUBLIC KEY
                #############################################################
                """ print("-------------------------------------------------")
                if  pem_data.strip() == public_key_pem.strip():
                    print("GENERATED PUB KEY == ORIGINAL PUB KEY")
                else:
                    print("GENERATED PUB KEY NOT EQUAL TO ORIGINAL PUB KEY")
                print("-------------------------------------------------") """
                
                
                ###################################################################################                
                # DECRYPT MESSAGE USING GENERATD PRIVATE KEY
                # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15
                ###################################################################################          
                try:    
                    decrypted_data = private_key.decrypt(encrypted_data, padding.PKCS1v15())
                    decrypted= True
                    """ print("----------------------------------------------------------------------------------")
                    print("Decrypted message: ", decrypted_data.decode())
                    print("==================================================================================") """
                    
                except:
                    try:
                        decrypted_data = private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                        decrypted= True
                        """ print("----------------------------------------------------------------------------------")
                        print("Decrypted message: ", decrypted_data.decode())
                        print("==================================================================================") """
                    except:
                        # obtain/print exception info
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        #traceback.print_tb(exc_traceback)
                        print("----------------------------------------------------------------------------------")
                        print("Decryption failed: "+f"{exc_type.__name__}: {exc_value}")
                        print("Public Key File  : ", file_a)
                        print("Encrypted File   : ", filename)
                        print("==================================================================================")

        else:
            continue
    
    if decrypted: 
        decrypted_files_counter +=1
        print("==================================================================================")
        print("Encrypted file: ",filename)
        print("Decrypted message: ", decrypted_data.decode())
        print("==================================================================================")
        print("q: ",q)
    print(f"Decrypted files : {decrypted_files_counter}/{file_counter}")