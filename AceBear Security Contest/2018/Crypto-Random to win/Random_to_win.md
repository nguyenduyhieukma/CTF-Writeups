
## Writeup for _Acebear Security Contest 1/2018_
### (Crypto challenge) _Random to win_
#### Tóm tắt đề bài
Cho dịch vụ tại _random2win.acebear.site:33337_ gồm 2 lựa chọn như sau:
- _Test_:
Người dùng gửi lên một thông điệp, thông điệp này được ánh xạ thành số nguyên `m`. Server sau đó trả về giá trị `c = (m + r*h) % p` với `h`,`p` là 2 thông số cố định, `r` là số nguyên ngẫu nhiên trong khoảng `(0, 222222)` có giá trị trong một phiên kết nối. Độ dài của `p` là 121 chữ số thập phân. Người dùng được phép _test_ 2 lần.
- _Submit_:
Server trả về giá trị `c = (m + r*h) % p`. Lần này, `m` và `r` là 2 số nguyên ngẫu nhiên trong khoảng `(10^10, 10^12)`. Nếu người dùng đoán được `m`, trả về _**FLAG**_

#### Ý tưởng giải quyết

- Từ `c1 = (m1 + r*h) % p` và `c2 = (m2 + r*h) % p`, dễ dàng suy ra `(m1-m2)-(c1-c2)` chia hết `p`. Như vậy, nếu ta chọn `m1, m2` sao cho `m1-m2` đủ lớn, tránh trường hợp `(m1-m2)-(c1-c2) = 0`, từ đó có thể tìm được `p`.  
- Sau khi có `p`, tính `h` theo công thức: `h = (c1-m1) * inverse(r) (mod p)`. Tuy `r` ngẫu nhiên nhưng khoảng giá trị bé (222221 khả năng) nên ta có thể vét cạn để được một danh sách gồm 222221 giá trị `h` có thể nhận. Tiếp tục với phiên làm việc khác cho ta một danh sách khác mà ta có thể dùng để đối chiếu tìm `h`.  
- Vấn đề cuối cùng là tìm `m` thỏa `m + r*h = c (mod p)` với `h`, `c`, `p` đã biết khi tiến hành _submit_. Do khoảng giá trị của `m`, `r` là tương đối lớn (gần `10^12` trường hợp) nên việc vét cạn là không khả thi. Để ý biến đổi phương trình trên một chút, ta được: `m + r*h = c + k*p` hay `c + k*p = m (mod h)`.Trong trường hợp này, vét cạn `k` để tìm `m` thỏa `10^10 < m < 10^12` sẽ dễ dàng hơn.

#### Thực hiện
**_B1:_** Kết nối đến server
(Thư viện _mylib.py_ được đính kèm ở cuối bài viết.)


```python
from mylib import *
setup('random2win.acebear.site', 33337)
connect()
```

**_B2:_** Chọn `m1 = 10^121`, `m2 = 0`. Gửi các giá trị lên server và nhận về `c1`, `c2` tương ứng.  
(Do `0 <= c1,c2 < p` nên `-p < (c1-c2) < p`, điều này đảm bảo `(m1-m2)-(c1-c2) > 10^121-p > 0`.)


```python
m1 = 10 ** 121
m2 = 0

send('1\n')
recvUntil('Message:') #synchronizing
send(long_to_bytes(m1))
c1 = int(recvUntil('[0-9]{2,}')[0]) #find at least 2-digit decimal number
send(long_to_bytes(m2))
c2 = int(recvUntil('[0-9]{2,}')[0])

print 'm1 = {}'.format(m1)
print 'm2 = {}'.format(m2)
print 'c1 = {}'.format(c1)
print 'c2 = {}'.format(c2)

```

    m1 = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    m2 = 0
    c1 = 309712032520002825110275326531818518716043951622854108685926951293705650894040448869625011828106953394701834734195763989
    c2 = 955895285012533811184600931620886903527398856295561008313865660384575752042965249419885624081202422462071920490447870794


**_B3:_** Tính `d = (m1-m2) - (c1-c2)`. Biết `d` chia hết cho `p`, suy ra `p`. Với cách chọn `m1`, `m2` như trên, nếu để ý, ta sẽ thấy tỉ số `d/p < 11`


```python
d = (m1-m2) - (c1-c2)
print 'd = {}'.format(d)
print 'Số chữ số thập phân của d: {}'.format(len(str(d)))
for i in range(11,1,-1):
    if d%i == 0:
        p = d/i
        break
print 'p = {}'.format(p)
print 'Số chữ số thập phân của p: {}'.format(len(str(p)))
```

    d = 10646183252492530986074325605089068384811354904672706899627938709090870101148924800550260612253095469067370085756252106805
    Số chữ số thập phân của d: 122
    p = 2129236650498506197214865121017813676962270980934541379925587741818174020229784960110052122450619093813474017151250421361
    Số chữ số thập phân của p: 121


**_B4:_** Tính danh sách `l1` gồm các giá trị có thể nhận của `h`. Thực hiện một kết nối khác đến server và tương tự tính danh sách `l2`, lấy tập giao gán lại cho `l1`: `l1 = l1 & l2` và lặp lại cho đến khi kích thước `l1 = 1`.


```python
l1 = [((c1-m1) * inverse(i,p)) % p for i in range(1,222222)] #using (c2, m2) yields the same result

while True:
    connect()
    send('1\n')
    recvUntil('Message:')
    send(long_to_bytes(m1))
    c1 = int(recvUntil('[0-9]{2,}')[0])
    l2 = [((c1-m1) * inverse(i,p)) % p for i in range(1,222222)]
    l1 = list(set(l1) & set(l2))
    print 'Kích cỡ tập giao: {}'.format(len(l1))
    if len(l1) == 1:
        h = l1[0]
        break

print 'h = {}'.format(h)
```

    Kích cỡ tập giao: 2
    Kích cỡ tập giao: 2
    Kích cỡ tập giao: 2
    Kích cỡ tập giao: 1
    h = 11305546770736405378819894875529407145124231011999396912086973074056791191623579252993880901245430834195596982773094


**_B5:_** Kết nối đến server và chọn mục _Test_ để nhận `c`. Vét cạn `k` trong công thức `c + k*p = m (mod h)` cho đến khi được `10^10 < m < 10^12`. Cũng cần chú ý rằng, vì `m < 10^12 << h` nên xác suất `m` ngẫu nhiên nhỏ hơn `10^12` là rất thấp. Cũng có thể giới hạn `k` thông qua công thức `m + r*h = c + k*p`.


```python
connect()
send('2\n')
c = int(recvUntil('[0-9]{2,}')[0])

kmin = (10**10 + 10**10 * h - c) // p + 1
kmax = (10**12 + 10**12 * h - c) // p
print 'kmin = {}; kmax = {}'.format(kmin, kmax)

for k in range(kmin, kmax+1):
    m = (c + k*p) % h
    if m < 10**12: break
print 'k = {}; m = {}'.format(k,m)

send(str(m))
flag = recvUntil('AceBear{.*}')[0]
print flag
```

    kmin = 53097; kmax = 5309670
    k = 1726857; m = 698100304859
    AceBear{r4nd0m_is_fun_in_my_g4m3}

#### Phụ lục
Đề bài: [random2win.tar.gz](./random2win.tar.gz)  
Thư viện: [mylib.py](./mylib.py)  
Just run and get flag (python version): [Random_to_win.py](./Random_to_win.py)
