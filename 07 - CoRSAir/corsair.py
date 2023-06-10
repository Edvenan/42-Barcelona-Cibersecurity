from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import argparse
import sys
import traceback
from utils import *


####################################################
# 1) GET PUBLIC KEY PEM FILES FROM PATH
####################################################
def get_pem_files(path:str) -> list:
    files = []
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                # if file has .pem extension, we add it to the 'files' list.
                if entry.name.split(sep=".")[-1] == "pem":
                    files.append(entry.path)
            return files
    except:
        # obtain/print exception info
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback)
            print(f"{exc_type.__name__}: {exc_value}\n")
            exit(2)

####################################################
# 2) EXTRACT EXPONENT & MODULUS FROM PUB KEY PEM FILES 
####################################################
def extract_publicKey_data(files:list) -> dict:
    pubkey_data = {}

    for file in files:

        # Read from file public key in PEM format 
        with open(file, "rb") as key_file:
            pem_data = key_file.read()
                    
        # Serialize the PEM-encoded public key (convert to RSAPublicKey object)
        try:
            public_key = serialization.load_pem_public_key(pem_data)

            #print(public_key.public_numbers())
            
            # pubkey_data = { filename : [exponen, modulus] }
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
            continue
    return pubkey_data

####################################################
# 3) FIND PRIVATE KEYS COMPARING MODULUS FROM FILES
####################################################
def find_privateKey(pubkey_data:dict) -> dict:
    # we will store regenerated private keys in a dict privKeys = { puKey filename : private_key }
    privKeys = {}

    global file_counter
    file_counter = 0
    # try find GCD betwewn modulus of two pubic keys
    # file_a = filename, data_a = [exponen, modulus]
    for file_a, data_a in pubkey_data.items():
        file_counter += 1

        for file_b, data_b in pubkey_data.items():
            if file_a != file_b:

                res_gcd = gcd(data_a[1], data_b[1])
                if res_gcd > 1:
                    # There is a common divisor so both modulus are not co-prime
                    
                    # we asume p = gcd
                    p = res_gcd         # int required
                    # q = n/p    
                    q = data_a[1]//p    # int required
                    e = data_a[0]
                    
                    # file_name where to store generated private_key
                    output_file = f"private_{file_a}"
                    
                    ###########################################
                    # Generate PEM+PKCS#8 Private key with the obtained parameters
                    ###########################################
                    pkcs8_private_key = generate_pkcs8_private_key(p, q, e, output_file)

                    if not pkcs8_private_key: 
                        continue

                    # Load the PEM-encoded private key
                    # reads the PEM-encoded private key data, performs the necessary parsing, and constructs a private key object that can be used
                    # for cryptographic operations. The resulting private_key object is an instance of the 
                    # cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey class (assuming an RSA private key).
                    private_key = serialization.load_pem_private_key(pkcs8_private_key.encode(), None)

                    privKeys[file_a] = private_key
                else:
                    continue
            else:
                continue
    # privKeys = { puKey_filename : privKey }
    return privKeys
                    
####################################################
# DECRYPT FILES WITH FOUND PRIV KEYS
####################################################                    
def decrypt_file(privKeys:dict) -> None:                    
    decrypted_files_counter = 0
    
    for file, private_key in privKeys.items():                
                      
        ########################################### 
        # LOAD ENCRYPTED DATA FROM FILE '.bin'
        ########################################### 
        filename = file.replace(".pem", ".bin")
        filename = filename.replace("pubkey", "ciphertext")

        with open(filename, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted = False
        #################################################################################################################                
        # DECRYPT MESSAGE USING GENERATD PRIVATE KEY (1) using PKCS1v15 padding (2) using OAEP padding + hash SHA256
        # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15
        #################################################################################################################          
        try:    
            decrypted_data = private_key.decrypt(encrypted_data, padding.PKCS1v15())
            decrypted= True
        except:
            try:
                decrypted_data = private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                decrypted= True
            except:
                # obtain/print exception info
                exc_type, exc_value, exc_traceback = sys.exc_info()
                #traceback.print_tb(exc_traceback)
                print("----------------------------------------------------------------------------------")
                print("Decryption failed: "+f"{exc_type.__name__}: {exc_value}")
                print("Public Key File  : ", file)
                print("Encrypted File   : ", filename)
                print("==================================================================================")

        
        if decrypted: 
            decrypted_files_counter +=1
            print("==================================================================================")
            print("Public Key File  : ", file)
            print("Encrypted file   : ",filename)
            print("Decrypted message: '{}'".format(decrypted_data.decode().strip("\n")))
            #print("p: {}\nq: {}\nn: {}".format(private_key.private_numbers().p, private_key.private_numbers().q, private_key.private_numbers().public_numbers.n))
            print("==================================================================================")
        print(f"Decrypted files : {decrypted_files_counter}/{file_counter}")
        
######################################
# MAIN
######################################
def main():
    
    # handle arguments input by user
    parser = argparse.ArgumentParser(description="(CoRSAir.py) This is a script aimed to crack an RSA private key and decrypt and encrypted file to prove it.\
        There are two requirements for this algorithm to work: (1) at least two public keys generated with the same cipher and (2) that the cipher used\
        employs a low entropy randome number generator. (2023, Eduard Vendrell)")
    
    parser.add_argument("path", type=str, help="Enter the folder path where to find the RSA public keys and encrypted files.")

    args = parser.parse_args()

    if args.path:
        # Clearing the Screen
        clean()

        pubKey_files = get_pem_files(args.path)
        pubkeys_data = extract_publicKey_data(pubKey_files)
        privKeys = find_privateKey(pubkeys_data)
        decrypt_file(privKeys)
      
    else:
        # No file specified
        print("Please specify a path")

if __name__ == '__main__':
    main()