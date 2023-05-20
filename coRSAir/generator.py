import argparse
import random
from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
from lorem.text import TextLorem
from loading import ft_progress


# RSA key generator function
def generate_rsa_keys(times):
    
    # Generate keys using the same 'p' value 
    p1 = 13223199974589313585283471854827363329451685303943205044027865131047695079691108706585803904203301545648101019060082323960067905432343412585098414381558929
    p2 = 13074358256206665105956844254872464791455783011218926315574506536899756094202061832400538633584249598415024636338845868462911949255730651995021077864973483
    p3 = 11083526568452982131964964676579415811827280156880822536123468319139375792482362247039287720519745289756730597874745518972168015316272870437159014052571633
    
    for i in ft_progress(range(times)):
        # select a random p value
        p = random.choice([p1, p2, p3])
        # Generate the co-prime number q
        q = generate_coprime(p)

        # Calculate the modulus n
        n = p * q

        # Calculate Euler's totient function phi
        phi = (p - 1) * (q - 1)

        # Choose a public exponent e
        e = 65537  # Commonly used public exponent

        # Calculate the private exponent d
        d = modinv(e, phi)

        # Create the RSA key object
        key = RSA.construct((n, e, d))

        # Save the public and private keys to files
        public_key_file = f"./keys/{i+1}_pubkey.pem"
        private_key_file = f"./keys/privateKeys/{i+1}_privkey.pem"
        os.makedirs(os.path.dirname(public_key_file), exist_ok=True)
        os.makedirs(os.path.dirname(private_key_file), exist_ok=True)
        
        with open(public_key_file, "wb") as f:
            f.write(key.publickey().export_key(format="PEM"))
        with open(private_key_file, "wb") as f:
            f.write(key.export_key(format="PEM"))
            
        # Encrypt a sentence using the pub key
        text_file_encrypter(key.publickey().export_key(format="PEM"), public_key_file)

# Helper function to get a random co-prime of 'p'
def generate_coprime(p):
    # Calculate the minimum and maximum values for q based on the number of digits in p
    min_value = 10 ** (len(str(p)) - 1)
    max_value = (10 ** len(str(p))) - 1

    # Start from the minimum value and check for a prime co-prime number
    rand = random.randint(1, 50)
    count = 0
    q = min_value
    while True:
        if q != p and (q%2 != 0):
            if is_prime(q):
                if (count == rand):
                    return q
                else:
                    count += 1
        q += 1
        if q > max_value:
            q = min_value

# Helper function to check if a number is prime
def is_prime(n, k=5):
    """Check if a number n is prime using Miller-Rabin primality test.
    
    Args:
        n (int): The number to check for primality.
        k (int): The number of iterations for the Miller-Rabin test (default: 5).
    
    Returns:
        bool: True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Write n-1 as 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Run Miller-Rabin primality test k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

# Helper function to calculate the modular inverse
def modinv(a, m):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = egcd(b % a, a)
            return gcd, y - (b // a) * x, x

    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        raise ValueError("The modular inverse does not exist.")
    return x % m

# text file encrypter
def text_file_encrypter(public_key, filename):
    """ # Load the RSA public key from the input file
    with open(filename, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read()) """

    public_key = serialization.load_pem_public_key(public_key)
    # Encrypt the message: a sentence of 5 or 6 words
    # Limit sentence max legth to 80 bytes so that it can 
    # be encrypted properly using OAEP padding, 256-bit hash
    # and a 1024-bit RSA key
    lorem = TextLorem(srange=(5,6))
    message = lorem.sentence().encode('ascii')[:80]
    
    ciphertext = public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Save the encrypted message to a new file with a .bin extension
    new_filename = filename.replace(".pem",".bin")
    new_filename = new_filename.replace("pubkey","ciphertext")
    
    with open(new_filename, "wb") as f:
        f.write(ciphertext)

    #print("Message encrypted and saved to:", new_filename)    



# Generate encrypted files
# read pub key files
""" files = []
with os.scandir('./keys/') as entries:
    for entry in entries:
        # if file has 'pubkey' prefix, we add it to the 'files' list.
        if entry.name.split(sep="_")[0] == "pubkey":
            files.append(entry.path)
for file in files:
    text_file_encrypter(file) """
            



######################################
# MAIN
######################################
def main():
    
    # handle arguments input by user
    parser = argparse.ArgumentParser(description="This is an ultralow entropy RSA keys generator.\nIt generates [n] RSA Keys and [n] encrypted\
        messages. RSA Keys are 1024-bit long and OAEP padding and hashing algorithm SHA-256 are used. The purpose of this geneator is to provide\
        keys that prove the vulnerability of RSA algorithm when using a low entropy generator. (2023, Eduard Vendrell)")
    
    parser.add_argument("number", type=int, help="Enter number of RSA keys and encrypted files to be generated.")

    args = parser.parse_args()

    if args.number:
        # Generate public Keys, private keys and encrypted files
        generate_rsa_keys(args.number)
      
    else:
        # No file specified
        print("Please specify a file")

if __name__ == '__main__':
    main()