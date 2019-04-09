
# Write-up for AceBear Security Contest 2019
## (Crypto challenge) _babyRSA_

### Challenge summary
Find $p$, $q$ given $n = pq$, $a = (p + q)^{2019}$ mod $n$ and $b = (p + 2019)^q$ mod $n$.

Challenge files: [rsa.py](resource/rsa.py).

### Suggested solution
Notice that $a \equiv p^{2019}$ (mod $q$) and $b \equiv p + 2019$ (mod $q$), we conclude that $a \equiv (b - 2019)^{2019} \equiv ((b - 2019)^{2019} $mod $n$) (mod $q$). Then $m = a - ((b - 2019)^{2019} $mod $n$) should be a multiple of $q$ and $GCD(m, n)$ should give us $q$.

### P.S.
I feel sorry for contestants who had spent more than 24 hours trying to complicate the problem and became frustrated. Please make your Number theory background stronger.
