
# Write-up for AceBear Security Contest 2019
## (Crypto challenge) _MD5 again?_

### Challenge summary
An improper implementation of MD5 was given and contestants were asked to reverse its state transition algorithm in order to forge arbitrary secret-prefix MACs without knowing the chunksize-long secret key.

Challenge files: [md5_again.py](resource/md5_again.py).

### Suggested solution
Based on the pseudocode given at [MD5 wikipedia page](https://en.wikipedia.org/wiki/MD5#Pseudocode), the missing part in the provided implementation in the challenge is:

```
    //Add this chunk's hash to result so far:
    a0 := a0 + A
    b0 := b0 + B
    c0 := c0 + C
    d0 := d0 + D
```

Therefore, the state transition is about to simply apply the main MD5 operation 64 times. The figure below describes one MD5 operation. Reversing it is not a hard task.

![the MD5 operation](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/MD5_algorithm.svg/300px-MD5_algorithm.svg.png)

### P.S.
A small change to a standard cryptography algorithm/protocol may cause you a lot of trouble.
