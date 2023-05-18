from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Path to the public_key.pem file
paths =["./sample/public.pem", "./2.pem"]
pubkeys = {}

for pubkey_path in paths:

    # Read the contents of the public_key.pem file
    with open(pubkey_path, "rb") as key_file:
        pem_data = key_file.read()
        
    # Load the PEM-encoded public key
    public_key = serialization.load_pem_public_key(pem_data, backend=default_backend())

    print(public_key.public_numbers())

    # Extract the exponent
    exponent = public_key.public_numbers().e

    # Extract the modulus
    modulus = public_key.public_numbers().n

    # Print the extracted values
    print("Exponent (e):", exponent)
    print("Modulus (n):", modulus)



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