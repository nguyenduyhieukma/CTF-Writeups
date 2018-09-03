## Isitdtu CTF 2018 (Qualification Round) Hints for Crypto challenges
-   Time: _July 28, 2018_
-   Place: _Online_
-   Website: _<https://ctf.isitdtu.com/>_

### XOR

(_100 pt, 65 solves_)

We can break the encryption process into 3 steps: `1st permutation` - `usual XOR` - `2nd permutation`. Since the key is only 10-byte long and we know that the FLAG starts with `ISITDTU{`, it is not hard to recover the key and the plaintext.

Challenge file: [xor.py](xor.py).

### Baby

(_271 pt, 46 solves_)

Knowing that `1 | x = 1` and `0 | x = x`, we can recover each i-th bit of the FLAG by comparing `hash(FLAG)` and `hash(FLAG | 2**i)`. If they are equal, the i-th bit should be 1, otherwise it is 0.

Challenge file: [baby.py](baby.py).

### Love Cryptography

(_424 pt, 41 solves_)

Notice that `'I'` and `'T'` are repeated twice in `'ISITDTU'`, we can search through the cipher list to obtained the encrypted numbers for `'I'`, `'S'`,`'T'`,`'D'`,`'U'`. Doing simple modular arithmetic reveals `m`, `n`, `c`. Since then, it's easy to decrypt the remaining numbers in the list.

Challenge file: [love_cryptography.py](love_cryptography.py).

### Simple RSA

(_534 pt, 37 solves_)

Since `p3 ~ 10*p2 ~ 100*p1 ~ 1000*p`, `p * p3 ~ p1 * p2`. Using Fermat method to factor `n = p*p1*p2*p3`, we would obtain `n1 = p * p3` and `n2 = p1 * p2`. Let's rewrite `p3` as `1000*p +r1` and `p2` as `10*p1 + r2` (`r1`, `r2` are small compared to those primes). This results in `n1 = p * (1000*p + r1)` and `n2 = p1 * (10*p1 + r2)`. Finding integer solutions to these equations helps us factor `n` completely.

Challenge file: [simple_rsa.py](simple_rsa.py).

### aes_cnv

(_871 pt, 20 solves_)

Ask the server to encrypt `'Give me the flaf'` which is a valid input, then complement the last bit of the IV block before send back to the server to get FLAG.

Challenge files : [AES_CNV.py](AES_CNV.py) and [challenge.py](challenge.py).

### ecc

(_995 pt, 5 solves_)

The elliptic-curve based pseudo-random number generator (PRNG) is broken since we know the discrete log of `Q` to the base `P`. Given an output, one can easily recover the seed and therefore, should be able to predict subsequent outputs. Notice that the PRNG only outputs 240/256 bits of the x-coordinate of `s.Q`, thus a 16-bit brute force on the remaining bits is needed to solve this task.

Challenge file: [ecc.py](ecc.py).
