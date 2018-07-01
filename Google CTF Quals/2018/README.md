# Google CTF 2018 (Qualification Round) Write-ups
- Time: _June 23-24, 2018_
- Place: _Online_
- Website: _https://capturetheflag.withgoogle.com/_

## Challenges with write-up available:
- **Crypto**:
  + _[DM COLLISION](Crypto-DM-COLLISION/README.md) (176 pt, 64 solves)_
  + _[DOGESTORE](Crypto-DOGESTORE/README.md) (267 pt, 27 solves)_

## Hints for other challenges:
### Crypto
#### BETTER ZIP
(_231 pt, 38 solves_)

Basic steps:
1. Reverse the LFSR, in other words, recover all possible `poly`'s, given the `iv` and some output.
2. Extract `encrypted_data`, `key_iv`, `cipher_iv` from the ZIP file given. If you don't want to examine the ZIP headers, just modify the source code to let it print the offsets while packing the data and run a test.
3. Using the `cipher_iv`, restore the first 20 bytes of the original PNG file.
4. Learn the PNG format to guess the next 20 bytes or more of the original PNG file. You may want to edit an image with MS Paint and save it in PNG format.
5. For each guess, derive the output of the 8 LFSRs, reverse them, recover the key, decrypt the `encrypted_data` and check if it is valid.

Challenge files: [Crypto-BETTER-ZIP.zip](Crypto-BETTER-ZIP.zip)

#### MITM
(_243 pt, 34 solves_)

Basic steps:
1. Send the little-endian byte representation of `2^255 - 19` as public key during the handshakes with both the server and the client since in the integers mod `2^255 - 19`, `0` and `2^255 - 19` are the same but the `2^255 -19` public key is not rejected by the vulnerable handshake protocol. More on [curve25519](https://en.wikipedia.org/wiki/Curve25519) and the [implementation](http://cr.yp.to/ecdh/curve25519-20051115.pdf) used by the challenge.
2. Now, you know the `sharedKey` between the parties. It's time to authenticate. Forward the server's nonce to the client.
3. Forward the client's proof to the server.
4. Now, you're authenticated and should be able to get the flag.

Challenge files: [Crypto-MITM.zip](Crypto-MITM.zip)

#### PERFECT SECRECY
(_158 pt, 74 solves_)

You need to learn about the RSA least significatn bit oracle attack.

Challenge files: [Crypto-PERFECT-SECRECY.zip](Crypto-PERFECT-SECRECY.zip)