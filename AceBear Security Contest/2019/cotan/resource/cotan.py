#!/usr/bin/env python3

# PART 1: the definition of G
from Crypto.Util.number import inverse
p = 1361129467683753853853498429727072846149


class G(object):
    @staticmethod
    def get_identity():
        return G("INF")

    def __init__(self, x):
        self.x = x

    def star(self, other):
        if self.x == "INF":
            return other
        if other.x == "INF":
            return self
        if (self.x + other.x) % p == 0:
            return G.get_identity()

        return G((self.x * other.x - 1) * inverse(self.x + other.x, p) % p)

    def repeated_star(self, n):
        s = G.get_identity()
        a = self
        while n > 0:
            if n & 1:
                s = s.star(a)
            a = a.star(a)
            n = n >> 1
        return s

    def __repr__(self):
        return repr(self.x)

    def __str__(self):
        return str(self.x)


# PART 2: all you need to get flag
import os
from Crypto.Cipher.AES import AESCipher
from secret import flag

key = os.urandom(16)
print(AESCipher(key).encrypt(flag.encode() + b"\x00" * (-len(flag) % 16)).hex())
# 4e8f206f074f895bde336601f0c8a2e092f944d95b798b01449e9b155b4ce5a5ae93cc9c677ad942c32d374419d5512c

k = int.from_bytes(key, "big")
g = G(2)
print(g.repeated_star(k))
# 675847830679148875578181214123109335717