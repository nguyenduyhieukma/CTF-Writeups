## Tokyo Western CTF 2018 (Qualification Round) Hints for some Crypto challenges
-   Time: _September 1-2, 2018_
-   Place: _Online_
-   Website: _<https://score.ctf.westerns.tokyo/>_

### scs7

(_112 pt, 134 solves_)

Base59 (each symbol in a ciphertext represents a number in the range 0-58).

Challenge file: None (black box)

### Revolutional Secure Angou

(_154 pt, 82 solves_)

`e*q = 1 (mod p)` implies that `e*q = k*p + 1` (1). Since `q < p`, we know that `k < e = 65537`. So, just brute-force `k` until we find a solution to the equation `e*n = k * p^2 + p` (2). Notice that (2) is (1) with both side multiplied by `p`.

Challenge file: [revolutional-secure-angou.7z](revolutional-secure-angou.7z).

### mixed cipher

(_233 pt, 39 solves_)

You need to:
-   Look for some multiples of the modulus `n`, then calculate the GCD to get `n`.
-   Learn how to decrypt arbitrary ciphertexts, given an RSA LSB(s) oracle, to get the AES key.
-   Learn how to untwist the Mersenne Twister (the `random` module's core PRNG) to predict the IV used to encrypt the flag.

Challenge file: [mixed_cipher.rar](mixed_cipher.rar).
