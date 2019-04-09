
# Write-up for AceBear Security Contest 2019
## (Crypto challenge) _cotan_

### Challenge summary
A description of the challenge was also provided along with the source code. Please have a look at cotan.pdf.

Challenge files: [cotan.pdf](resource/cotan.pdf), [cotan.py](resource/cotan.py).

### Suggested solution
Let $f(x) = \frac{(x + i)}{(x - i)}$ with $i^2 = -1$; then $f$ is a homomorphism between the group $(G, \star)$ (defined in cotan.py) and $(F_p^*, \cdot)$ (verified below). Since $p$ was chosen such that $(p-1) \vdots 4$, so $i \in F_p$ and the discrete logarithm problem (DLP) in $(G, \star)$ has been completely reduced to DLP in $(F_p^*, \cdot)$. There are sub-exponential algorithms to solve this kind of problem in $F_p$. When $p$ is about 128-bit long, it can be done in a few minutes by a normal laptop with SageMath installed.


```python
var("a,b")
star(a, b) = (a*b - 1)/(a + b)
f(x) = (x + I)/(x - I)

print f(star(a, b)).simplify_rational()
print (f(a) * f(b)).simplify_rational()
print bool(f(star(a, b)) == f(a) * f(b))
```

    ((a + I)*b + I*a - 1)/((a - I)*b - I*a - 1)
    ((a + I)*b + I*a - 1)/((a - I)*b - I*a - 1)
    True


How can one think of a homomorphism like this? Well, if one is familiar with power series, he/she will know the formula $e^{i\phi} = cos\phi + i.sin\phi$ and be able to express trigonometric functions like $sin$, $cos$, $tan$, $cotan$, ... in terms of the complex exponential. The $cotan$ function is indeed: $cot(x) = i\frac{e^{i2x} + 1}{e^{i2x} - 1}$. And as a consequence, $e^{i2x} = \frac{cot(x) + i}{cot(x) - i}$:


```python
var("cotx")
solve(cotx == I * (e^(I*2*x) + 1) / (e^(I*2*x) - 1), e^(I*2*x))
```




    [e^(2*I*x) == (cotx + I)/(cotx - I)]



Now, if $cot(x) \xrightarrow{f} e^{i2x}$, $cot(y) \xrightarrow{f} e^{i2y}$, then $cot(x) \star cot(y) = cot(x+y) \xrightarrow{f} e^{i2(x+y)} = e^{i2x}.e^{i2y}$ as expected.

### Another approach
A player from Meepwn team (@bmtd) had an idea of relate the `repeated_star` operation to the power of a matrix. I gave it a try during the event, and it turned out that, this approach can help to solve the problem too.

Basically, we can let $(a, b)$ represent $t = \frac{a}{b}$ ($a, b \in F_{p}$, $t \in G$), then the identity of $G$ and the generator are represented as $(1, 0)$ and $(2, 1)$ respectively. The result of the operation $\star$ between an arbitrary element $(a, b)$ and the generator $(2, 1)$ can be expressed as $(\frac{a}{b}.2 - 1, \frac{a}{b} + 2)$ or equivalently $(2a - b, a + 2b) = (a, b) \cdot A$ with $A = \begin{bmatrix} 2 & 1 \\ -1 & 2 \end{bmatrix}$.

Consequently, `repeated_star` of the generator $k$ times can be expressed as $(1, 0)\cdot A^k$. In this situation, we would want to diagonalize $A$ as $P \Lambda P^{-1}$ with $\Lambda = \begin{bmatrix} \lambda_1 & 0 \\ 0 & \lambda_2 \end{bmatrix}$. As a result, $(1, 0) \cdot P \cdot \begin{bmatrix} \lambda_1^k & 0 \\ 0 & \lambda_2^k \end{bmatrix} \cdot P^{-1}$ represents $g^{\star k}$ (`g.repeated_star(k)`).

After perform matrix multiplication, we will end up with an equation of the form $\frac{c_1 \lambda_1^{k} + c2 \lambda_2^{k}}{c_3 \lambda_1^{k} + c4 \lambda_2^{k}} = g^{\star k}$, which can be further reduced to $(\frac{\lambda_1}{\lambda_2})^k = c_5$. Again, this is DLP in $F_p$.

### P.S.
I hope you found this challenge interesting, or, at least learned something while trying to solve it.
