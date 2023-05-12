import hmac
import hashlib
import struct
import time

def generateTOTP(key, time, returnDigits, crypto):
    codeDigits = int(returnDigits)
    result = None

    # Using the counter
    # First 8 bytes are for the movingFactor
    # Compliant with base RFC 4226 (HOTP)
    while len(time) < 16:
        time = "0" + time

    # Get the HEX in a Byte[]
    msg = bytes.fromhex(time)
    k = bytes.fromhex(key)

    hash = hmac.new(k, msg, hashlib.__dict__[crypto]).digest()

    # put selected bytes into result int
    offset = hash[-1] & 0xf

    binary = ((hash[offset] & 0x7f) << 24) | \
             ((hash[offset + 1] & 0xff) << 16) | \
             ((hash[offset + 2] & 0xff) << 8) | \
             (hash[offset + 3] & 0xff)

    otp = binary % 10**codeDigits

    result = str(otp)
    while len(result) < codeDigits:
        result = "0" + result
    return result

# Seed for HMAC-SHA1 - 20 bytes
seed = "3132333435363738393031323334353637383930"
# Seed for HMAC-SHA256 - 32 bytes
seed32 = "3132333435363738393031323334353637383930" + "313233343536373839303132"
# Seed for HMAC-SHA512 - 64 bytes
seed64 = "3132333435363738393031323334353637383930" + \
         "3132333435363738393031323334353637383930" + \
         "3132333435363738393031323334353637383930" + \
         "31323334"

T0 = 0
X = 30
testTime = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]

steps = "0"

print("+---------------+-----------------------+------------------+--------+--------+")
print("|  Time(sec)    |   Time (UTC format)   | Value of T(Hex)  |  TOTP  | Mode   |")
print("+---------------+-----------------------+------------------+--------+--------+")

for i in range(len(testTime)):
    T = (testTime[i] - T0) // X
    steps = format(T, '016X')
    fmtTime = "{:<11}".format(str(testTime[i]))
    utcTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(testTime[i]))
    print("|  {}  |  {}  | {} |".format(fmtTime, utcTime, steps), end="")
    print(generateTOTP(seed, steps, "8", "SHA1") + "| SHA1   |")
    print("|  {}  |  {}  | {} |".format(fmtTime, utcTime, steps), end="")
    print(generateTOTP(seed32, steps, "8", "SHA256") + "| SHA256 |")
    print("|  {}  |  {}  | {} |".format(fmtTime, utcTime, steps), end="")
    print(generateTOTP(seed64, steps, "8", "SHA512") + "| SHA512 |")
    print("+---------------+-----------------------
