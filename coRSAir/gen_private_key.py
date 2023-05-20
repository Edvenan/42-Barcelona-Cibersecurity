import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64
import random
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from math import sqrt


####################################################
# GCD
####################################################
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
###################################################


#####################################################################
#   IS PRIME ?
#####################################################################
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


#####################################################################
#   RECOVER KEY
#####################################################################
def recover_key(p, q, e, output_file):
    """Recovers an RSA private key from:
        p: Prime p
        q: Prime q
        e: Public exponent
        output_file: File to write PEM-encoded private key to"""

    # SRC: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    def egcd(a, b):
        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
        return gcd, x, y

    def modinv(a, m):
        gcd, x, y = egcd(a, m)
        if gcd != 1:
            return None  # modular inverse does not exist
        else:
            return x % m

    def generate_pkcs8_private_key(p, q, e, d):
        # Calculate the modulus and private exponent
        n = p * q
        d = d

        # Create a private key object
        private_key = rsa.RSAPrivateNumbers(
            p=p,
            q=q,
            d=d,
            dmp1=rsa.rsa_crt_dmp1(d, p),
            dmq1=rsa.rsa_crt_dmq1(d, q),
            iqmp=rsa.rsa_crt_iqmp(p, q),
            public_numbers=rsa.RSAPublicNumbers(e=e, n=n)
        ).private_key()

        # Serialize the private key in PKCS#8 format
        pkcs8_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        return pkcs8_private_key.decode('ascii')

    n = p * q
    phi = (p - 1) * (q - 1)   # Totient
    d = modinv(e, phi)
    dp = modinv(e, (p - 1))
    dq = modinv(e, (q - 1))
    qi = modinv(q, p)

    """ print("p: ",p)
    print("n: ",n)
    print("e: ",e)
    print("d: ",d)
    print("dp: ",dp)
    print("dq: ",dq) """

    if not d: return None
    ###################################
    # CALC PRIVATE KEY USING PKCS8
    ###################################
    private_key_pkcs8 = generate_pkcs8_private_key(p, q, e, d)
    """ print("PKCS8: ({})".format(len(private_key_pkcs8)))
    print(private_key_pkcs8) """
    
    # WRITE PRIVATE KEY TO FILE
    """ with open(output_file, "w") as f:
        f.write(pkcs8_private_key) """
    
    # RETURN PRIVATE KEY USING PKCS8 
    return private_key_pkcs8

