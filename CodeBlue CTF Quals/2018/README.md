## CodeBlue CTF 2018 (Qualification Round) Hints for Crypto challenges
-   Time: _July 29, 2018_
-   Place: _Online_
-   Website: _<https://score.ctf.codeblue.jp/>_

### lagalem

(_246 pt, 35 solves_)

Given `c2 = m * h^r mod p` and `c2_ = m * h^(A*r+B) mod p`, just eliminate `r` and solve for `m`.

Challenge files: [problem.py](problem.py) and [transcript.txt](transcript.txt).

### LED

(_315 pt, 19 solves_)

Basic steps:
1.  Study the LED block cipher, reverse all the primitive operations (`MixColumn`, `ShiftRow`, `SubCell`,...).
2.  Reverse the final permutation of the lazy-mode encryption. (Tip: thinking about what would happen after one round if we change only 1 bit (or 1 nibble, especially those on the first row) of the plaintext).
3.  Recover the first 64 bits of the key by asking the server to encrypt a plaintext in 1-round, lazy mode.
4.  Recover the remaining 64 bits of the key by asking the server to encrypt a same plaintext twice, in 4-round and 5-round, lazy mode.

Challenge files: [problem_final.py](problem_final.py).
