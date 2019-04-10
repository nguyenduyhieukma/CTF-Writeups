
# Write-up for AceBear Security Contest 2019
## (Crypto challenge) _cotan_

### Challenge summary
A description of the challenge was also provided along with the source code. Please have a look at cotan.pdf.

Challenge files: [cotan.pdf](resource/cotan.pdf), [cotan.py](resource/cotan.py).

### Suggested solution
Let <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/267dd1b74101f060100170e6315e8b61.svg?invert_in_darkmode" align=middle width=88.54138755pt height=33.2053986pt/> with <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/6c9dcbb7c305a5530e5f3c4d3296dc08.svg?invert_in_darkmode" align=middle width=55.95995955pt height=26.7617526pt/>; then <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/190083ef7a1625fbc75f243cffb9c96d.svg?invert_in_darkmode" align=middle width=9.81741585pt height=22.8310566pt/> is a homomorphism between the group <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/9228471039d5ead08f5b33cc12ffa732.svg?invert_in_darkmode" align=middle width=41.2351698pt height=24.657534pt/> (defined in cotan.py) and <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/266cecf8a7ec9ba833a22f09b3932df8.svg?invert_in_darkmode" align=middle width=45.0685521pt height=24.657534pt/> (verified below). Since <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.27056725pt height=14.1552444pt/> was chosen such that <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/759bbf515d31d2b59bd2fde765f5f5a7.svg?invert_in_darkmode" align=middle width=62.1518337pt height=29.7716892pt/>, so <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/30e81b566c3b57ff473a510d3338a3c2.svg?invert_in_darkmode" align=middle width=43.1016399pt height=22.4657235pt/> and the discrete logarithm problem (DLP) in <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/9228471039d5ead08f5b33cc12ffa732.svg?invert_in_darkmode" align=middle width=41.2351698pt height=24.657534pt/> has been completely reduced to DLP in <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/266cecf8a7ec9ba833a22f09b3932df8.svg?invert_in_darkmode" align=middle width=45.0685521pt height=24.657534pt/>. There are sub-exponential algorithms to solve this kind of problem in <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/2c17c03ea35ba6da96125ac9680b37a1.svg?invert_in_darkmode" align=middle width=17.347275pt height=22.4657235pt/>. When <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.27056725pt height=14.1552444pt/> is about 128-bit long, it can be done in a few minutes by a normal laptop with SageMath installed.


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


How can one think of a homomorphism like this? Well, if one is familiar with power series, he/she will know the formula <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/4e4b8acc9a39b105a0f28939d82b4fd5.svg?invert_in_darkmode" align=middle width=138.8813217pt height=27.9124395pt/> and be able to express trigonometric functions like <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/d9a2d241e661f6a9634e7c5de2864b39.svg?invert_in_darkmode" align=middle width=23.23558215pt height=21.6830097pt/>, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/270137a73ab17534918603dd63ca7024.svg?invert_in_darkmode" align=middle width=22.7873349pt height=14.1552444pt/>, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/84b314bc659e84e2ceabd09a45f9116d.svg?invert_in_darkmode" align=middle width=24.4921281pt height=20.2218027pt/>, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/6f9f3af460cb8f3ca1f5423db7cc40ab.svg?invert_in_darkmode" align=middle width=39.5739828pt height=20.2218027pt/>, ... in terms of the complex exponential. The <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/6f9f3af460cb8f3ca1f5423db7cc40ab.svg?invert_in_darkmode" align=middle width=39.5739828pt height=20.2218027pt/> function is indeed: <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/4e0773256d0b6015649b264923696520.svg?invert_in_darkmode" align=middle width=113.12332185pt height=33.8217429pt/>. And as a consequence, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/0eccd4a3153212f4b803fda243a9bcf9.svg?invert_in_darkmode" align=middle width=101.0064264pt height=33.2053986pt/>:


```python
var("cotx")
solve(cotx == I * (e^(I*2*x) + 1) / (e^(I*2*x) - 1), e^(I*2*x))
```




    [e^(2*I*x) == (cotx + I)/(cotx - I)]



Now, if <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/3ada0658ab3f87130b5424723ce5ad1a.svg?invert_in_darkmode" align=middle width=96.81928245pt height=36.1711977pt/>, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/0c0b25f28e244cb1e3d9b540ccfc6362.svg?invert_in_darkmode" align=middle width=95.69873445pt height=36.1711977pt/>, then <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/fdc8feb478db8524434f972c9e08eab9.svg?invert_in_darkmode" align=middle width=356.4749595pt height=36.1711977pt/> as expected.

### Another approach
A player from Meepwn team (@bmtd) had an idea of relating the `repeated_star` operation to the power of a matrix. I gave it a try during the event, and it turned out that, this approach can help to solve the problem too.

Basically, we can let <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/ba933e77b90dc996befbe81f77f43887.svg?invert_in_darkmode" align=middle width=35.8352676pt height=24.657534pt/> represent <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/2fdb55f42885e395bcc53e6476f47048.svg?invert_in_darkmode" align=middle width=36.95670825pt height=22.8532755pt/> (<img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/f1086a9271f9481e00dd7d66f3f3496e.svg?invert_in_darkmode" align=middle width=60.4882476pt height=22.8310566pt/>, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/4a7b92ef9c527f319d5a9b8b18877ccd.svg?invert_in_darkmode" align=middle width=38.95187835pt height=22.4657235pt/>), then the identity of <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/5201385589993766eea584cd3aa6fa13.svg?invert_in_darkmode" align=middle width=12.92464305pt height=22.4657235pt/> and the generator are represented as <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/f1a388999a6927863f4cc438232ccd6d.svg?invert_in_darkmode" align=middle width=36.5297361pt height=24.657534pt/> and <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/216d7efdb6b574766dfb2f986bb58981.svg?invert_in_darkmode" align=middle width=36.5297361pt height=24.657534pt/> respectively. The result of the operation <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/239f0fec4e07802db7bd8c11974f65e8.svg?invert_in_darkmode" align=middle width=8.21920935pt height=15.2968299pt/> between an arbitrary element <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/ba933e77b90dc996befbe81f77f43887.svg?invert_in_darkmode" align=middle width=35.8352676pt height=24.657534pt/> and the generator <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/216d7efdb6b574766dfb2f986bb58981.svg?invert_in_darkmode" align=middle width=36.5297361pt height=24.657534pt/> can be expressed as <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/1fab95b10d8b7ec8089059edf593390d.svg?invert_in_darkmode" align=middle width=111.64869705pt height=24.657534pt/> or equivalently <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/1239b38a57c8df015749fc0fb11370fb.svg?invert_in_darkmode" align=middle width=190.15369725pt height=24.657534pt/> with <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/1a4f044c293a78f2850627dbae8ababa.svg?invert_in_darkmode" align=middle width=104.1096441pt height=47.6716218pt/>.

Consequently, `repeated_star` of the generator <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.07536795pt height=22.8310566pt/> times can be expressed as <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/dbff3156852a893a00667557f6079736.svg?invert_in_darkmode" align=middle width=67.99654455pt height=27.9124395pt/>. In this situation, we would want to diagonalize <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879835pt height=22.4657235pt/> as <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/fe00657bc5e7369abe5fcd9f0343529e.svg?invert_in_darkmode" align=middle width=53.91565575pt height=26.7617526pt/> with <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/d1a3351e2951e17c208d306b264f8f6d.svg?invert_in_darkmode" align=middle width=107.8996413pt height=47.6716218pt/>. As a result, <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/a35940a241fded49e6bbe416a35fe363.svg?invert_in_darkmode" align=middle width=190.6392279pt height=47.9673546pt/> represents <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/2ecafcfcdf29b12a271afca5707e94c6.svg?invert_in_darkmode" align=middle width=22.4315817pt height=27.9124395pt/> (`g.repeated_star(k)`).

After perform matrix multiplication, we will end up with an equation of the form <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/716e7294dda73ad361a8fb2e251db4d7.svg?invert_in_darkmode" align=middle width=111.0965724pt height=38.104044pt/>, which can be further reduced to <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/cc822323a943fff9690d70bade48832b.svg?invert_in_darkmode" align=middle width=74.6149998pt height=29.461113pt/>. Again, this is DLP in <img src="https://rawgit.com/nguyenduyhieukma/CTF-Writeups/master/svgs/2c17c03ea35ba6da96125ac9680b37a1.svg?invert_in_darkmode" align=middle width=17.347275pt height=22.4657235pt/>.

### P.S.
I hope you found this challenge interesting, or, at least learned something while trying to solve it.
