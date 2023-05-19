import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa




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

    # SRC: http://crypto.stackexchange.com/questions/25498/how-to-create-a-pem-file-for-storing-an-rsa-key/25499#25499
    def pempriv(n, e, d, p, q, dP, dQ, qInv):
        template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
        seq = pyasn1.type.univ.Sequence()
        for i,x in enumerate([0, n, e, d, p, q, dP, dQ, qInv]):
            seq.setComponentByPosition(i, pyasn1.type.univ.Integer(x))
        der = pyasn1.codec.der.encoder.encode(seq)
        return template.format(base64.encodebytes(der).decode('ascii'))
    
    def generate_pkcs8_private_key(private_key):
    
        pkcs8_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pkcs8_private_key

    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    dp = modinv(e, (p - 1))
    dq = modinv(e, (q - 1))
    qi = modinv(q, p)

    #key = pempriv(n, e, d, p, q, dp, dq, qi)
    public_numbers = rsa.RSAPublicNumbers(e, n)
    key = rsa.RSAPrivateNumbers(p, q, d, dp,dq,qi, public_numbers).private_key()
    pkcs8_private_key = generate_pkcs8_private_key(key)

    """ with open(output_file, "w") as f:
        f.write(pkcs8_private_key) """
        
    return pkcs8_private_key

