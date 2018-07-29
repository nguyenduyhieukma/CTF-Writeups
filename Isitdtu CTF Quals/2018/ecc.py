from random import randint
from sys import argv, stdout

from fastecdsa.curve import P256
from fastecdsa.point import Point
from mathutil import p256_mod_sqrt, mod_inv
def gen_point():
    P = P256.G  
    d = randint(2, P256.q)  
    e = mod_inv(d, P256.q)  
    Q = e * P 
    assert(d * Q == P)    
    return P, Q, d

class gen_ECC():
    def __init__(self, seed, P, Q):
        self.seed = seed
        self.P = P
        self.Q = Q

    def genbits(self):
        t = self.seed
        s = (t * self.P).x
        self.seed = s
        r = (s * self.Q).x
        return r & (2**(8 * 30) - 1)  # return 30 bytes

#

def main():
    P, Q, d = gen_point()
    # P = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5, curve=P256)
    # Q = Point(0x43595b13c9dc2e7e6fdc09175a5527c4973778d96a9e602fc5bf35d7f8f43424, 0xda93baf3284401b5426dea5354e63738817ff4938f9532157ccff8535f6d1076, curve=P256)
    # d = 0xe7366b3509adb3de385d04712f8556c1cca77ee91d7e7df1fcfbd902c127d744

    e = gen_ECC(20639247711360085, P, Q)
    tmp = e.genbits()
    secret = e.genbits()
    print secret
    _flag = secret & (2**(8*28) - 1)
    # flag is ISITDTU{_flag} with _flag is int
    focus = (tmp << (2 * 8)) | (secret >> (28 * 8))
    print focus
    # 0x56929a811a2ac18732371d1615c937d92c61204481c746c9f836febf862b6096


if __name__ == '__main__':
    main()
