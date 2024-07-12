"""
Function `get_totp_token` generate time-based one-time (TOTP) password based on `secret`.
"""
import base64
import hashlib
import hmac
import struct
import time


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    # decoding our key
    msg = struct.pack(">Q", intervals_no)
    # conversions between Python values and C structs represente
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = o = h[19] & 15
    # Generate a hash using both of these. Hashing algorithm is HMAC
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    # unpacking
    return h


def get_progress():
    """
    Returns an integer number in range 0 - 29
    """
    t = int(time.time())
    return t % 30


def get_totp_token(secret):
    """
    Parameter `secret` must be a base32-encoded string.
    Returns 6-digit time-based password/token.
    """
    # ensuring to give the same otp for 30 seconds
    x = str(get_hotp_token(secret, intervals_no=int(time.time())//30))
    # adding 0 in the beginning till OTP has 6 digits
    while len(x) != 6:
        x += '0'
    return x  # base64 encoded key


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Secret token expected.")

    secret = sys.argv[1]
    print("TOTP:", get_totp_token(secret))
