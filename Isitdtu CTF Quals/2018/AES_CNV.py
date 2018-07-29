from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from time import ctime
from Secret import __SECRET__
import os

BLOCK_SIZE = 16

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def toblock(s):
    rs = []
    for i in range(0, len(s), BLOCK_SIZE):
        rs.append(s[i:i+BLOCK_SIZE])
    return rs

def tostr(src):
    s = ''.join(x for x in src)
    return s
    
def xor(dest, src):
    if len(dest) == 0:
        return src
    elif len(src) == 0:
        return dest
    elif len(dest) >= len(src):
        return ''.join(chr(ord(dest[i])^ord(src[i])) for i in range(len(src)))
    else:
        return ''.join(chr(ord(dest[i])^ord(src[i])) for i in range(len(dest)))


class AES_CNV():
    """
    AES CNV created by chung96vn of AceBear Team
    """
    def __init__(self, key):
        """
        Init object
        """
        assert len(key) == BLOCK_SIZE * 2
        self.key = key

    def encrypt(self, plain_text, iv):
        """
        Encrypt plaint text
        """
        assert len(iv) == 16
        plain_text = pad(plain_text)
        assert len(plain_text)%BLOCK_SIZE == 0
        cipher_text = ''
        aes = AES.new(self.key, AES.MODE_ECB)
        h = iv
        for i in range(len(plain_text)//BLOCK_SIZE):
            block = plain_text[i*16:i*16+16]
            block = xor(block, h)
            cipher_block = aes.encrypt(block)
            cipher_text += cipher_block
            h = md5(cipher_block).digest()
        return b64encode(iv+cipher_text)
        
    def decrypt(self, cipher_text):
        """
        Decrypt cipher text
        """
        cipher_text = b64decode(cipher_text)
        assert len(cipher_text)%BLOCK_SIZE == 0
        iv = cipher_text[:16]
        cipher_text = cipher_text[16:]
        aes = AES.new(self.key, AES.MODE_ECB)
        h = iv
        plain_text = ''
        for i in range(len(cipher_text)//BLOCK_SIZE):
            block = cipher_text[i*16:i*16+16]
            plain_block = aes.decrypt(block)
            plain_block = xor(plain_block, h)
            plain_text += plain_block
            h = md5(block).digest()
        return unpad(plain_text)

        
class Game():
    """
    Game for player
    """
    def __init__(self):
        self.key = os.urandom(BLOCK_SIZE*2)
        self.aes = AES_CNV(self.key)
        self.secret = toblock(pad(__SECRET__))
        
    def encode(self, m):
        m_ar = toblock(pad(m))
        p_ar = []
        for i in range(len(m_ar)):
            p_ar.append(xor(m_ar[i], self.secret[i%len(self.secret)]))
        p = tostr(p_ar)
        return self.aes.encrypt(p, os.urandom(BLOCK_SIZE))
        
    def decode(self, c):
        p = self.aes.decrypt(c)
        p_ar = toblock(p)
        m_ar = []
        for i in range(len(p_ar)):
            m_ar.append(xor(p_ar[i], self.secret[i%len(self.secret)]))
        m = tostr(m_ar)
        return unpad(m)
        