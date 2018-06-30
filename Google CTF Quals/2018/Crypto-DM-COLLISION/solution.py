#!/usr/bin/env python3
key1   = b'\x00' * 8
block1 = b'\x00' * 8

key2   = b'\x00' * 7 + b'\x01'
block2 = block1

from not_des import * 
WEAK_KEY = b'\xff' * 8 
L = list(KeyScheduler(Str2Bits(WEAK_KEY)))
S = set(map(tuple, L)) 

a = [None] * 18
a[8] = a[9] = Str2Bits(b'c001')

subkey = S.pop()
def f(block): return CipherFunction(subkey, block)

for i in range(10,18):
    a[i] = Xor(a[i-2], f(a[i-1]))

for i in range(7,-1,-1):
    a[i] = Xor(a[i+2], f(a[i+1]))

key3 = WEAK_KEY
def InvIP(block): return [block[IP_INV[i] - 1] for i in range(64)]
block3 = Bits2Str(InvIP(a[0] + a[1]))

from socket import create_connection
sock = create_connection(('dm-col.ctfcompetition.com', 1337))

sock.send(key1)
sock.send(block1)
sock.send(key2)
sock.send(block2)
sock.send(key3)
sock.send(block3)

print(sock.recv(4096))