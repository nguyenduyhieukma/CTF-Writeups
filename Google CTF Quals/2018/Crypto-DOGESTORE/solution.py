#!/usr/bin/env python3
KEY_SIZE = 110
KEYSTREAM = bytearray(KEY_SIZE)

def decrypt(encrypted): return bytes(a ^ b for a, b in zip(encrypted, KEYSTREAM))

def decode(encoded):
    s = b''
    for i in range(0, len(encoded), 2):
        s += bytes([encoded[i]]) * (encoded[i+1] + 1)
    return s

from hashlib import sha3_256
def hash(data): return sha3_256(data).digest()

def make_data(*ivvs):
    '''This function returns 110-byte data, default to all zeros.
    User can specify some (index, value_1, value_2)'s to modify the data as needed.
    '''
    data = bytearray(110)
    for ivv in ivvs:
        data[ivv[0]] = ivv[1]
        data[ivv[0]+1] = ivv[2]
    return bytes(data)

from socket import create_connection
ADDR = ('dogestore.ctfcompetition.com', 1337)
def post(data):
    'This function posts data to the server and returns the hash received'
    while True:
        try:
            sock = create_connection(ADDR)
            sock.send(data)
            return sock.recv(4096)
        except: pass
        
def post_data(*ivvs): return post(make_data(*ivvs))

DELTA = bytearray(KEY_SIZE - 2)
for i in range(0, len(DELTA), 2):
    print('Currnet index: {}/{}'.format(i, KEY_SIZE-2))
    
    for x in range(256):
        print('Trying x = {}... '.format(x), end='')
        
        _a = post_data((i, 0, 0), (i+2, x, 0))
        _b = post_data((i, 0, 1), (i+2, x, 1))
        if _a == _b:
            DELTA[i] = x
            DELTA[i + 1] = 1
            break
    
        _c = post_data((i, 0, 1), (i+2, x, 0))
        _d = post_data((i, 0, 0), (i+2, x, 1))
        if _c == _d:
            DELTA[i] = x
            DELTA[i + 1] = 0
            break
            
        print('Not matched!')
    
    print('Matched!')
    print('k[{}] XOR k[{}] = {}'.format(i, i+2, x))

    for j in range(1,8):
        _e = post_data((i, 0, 1<<j), (i+2, x, 1<<j))
        if _e == _a:
            DELTA[i + 1] |= (1<<j)
    
    print('k[{}] XOR k[{}] = {}'.format(i+1, i+3, DELTA[i+1]))
# DELTA = bytearray(b'\xbfIw\x90\x84\xba\xbc\xd9\xabv\xf2$!_\x0f\xd32\x1b\x00* 5\x82\xc9n\x9f3\xff9\x16$il^\xdf\xac\x84\x800w:\xaa/\x1c\xbe\x9d\x90\xb76rsk\xfa1[\xf8\r\x93\x10\xf1\x19\x99\xc1\x81\xb2\xc7\x1a%s3\x8cT\xe7\xfaA#c\xeb\xb4\xe1\xdd\xc5y\xcd\\)\xce\xe6\x10\x81@k\x98\xf8\xb5#\xe7\xc5\xe4\x8e\x88:\x95\xcc\xb14\xed\x15')

def keystream_init(k0, k1):
    KEYSTREAM[0] = k0
    KEYSTREAM[1] = k1
    for i in range(2, KEY_SIZE):
        KEYSTREAM[i] = DELTA[i-2] ^ KEYSTREAM[i-2]

with open('encrypted_secret','rb') as f:
    encrypted_secret = f.read()

for k0 in range(256):
    keystream_init(k0, 0) # the second argument is not important
    letters = decrypt(encrypted_secret)[::2] # focus on even-indexed bytes
    if b'CTF{' in letters:
        break
        
PATTERN = b'T\x00F\x00{'
for k1 in range(256):
    keystream_init(k0, k1) 
    decrypted_string = decrypt(encrypted_secret)
    if PATTERN in decrypted_string:
        break

secret = decode(decrypted_string)
print(secret)