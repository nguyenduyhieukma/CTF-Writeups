
# coding: utf-8

# ## Writeups for _Acebear Security Contest 1/2018_
# ### (Crypto challenge) _Random to win_
# #### Tóm tắt đề bài
# Cho dịch vụ tại _random2win.acebear.site:33337_ gồm 2 lựa chọn như sau:
# - _Test_:
# Người dùng gửi lên một thông điệp, thông điệp này được ánh xạ thành số nguyên `m`. Server sau đó trả về giá trị `c = (m + r*h) % p` với `h`,`p` là 2 thông số cố định, `r` là số nguyên ngẫu nhiên trong khoảng `(0, 222222)` có giá trị trong một phiên kết nối. Độ dài của `p` là 121 chữ số thập phân. Người dùng được phép _test_ 2 lần.
# - _Submit_:
# Server trả về giá trị `c = (m + r*h) % p`. Lần này, `m` và `r` là 2 số nguyên ngẫu nhiên trong khoảng `(10^10, 10^12)`. Nếu người dùng đoán được `m`, trả về _**FLAG**_
#
# #### Ý tưởng giải quyết
#
# - Từ `c1 = (m1 + r*h) % p` và `c2 = (m2 + r*h) % p`, dễ dàng suy ra `(m1-m2)-(c1-c2)` chia hết `p`. Như vậy, nếu ta chọn `m1, m2` sao cho `m1-m2` đủ lớn, tránh trường hợp `(m1-m2)-(c1-c2) = 0`, từ đó có thể tìm được `p`.
# - Sau khi có `p`, tính `h` theo công thức: `h = (c1-m1)*inverse(r) (mod p)`. Tuy `r` ngẫu nhiên nhưng khoảng giá trị bé (222221 khả năng) nên ta có thể vét cạn để được một danh sách gồm 222221 giá trị `h` có thể nhận. Tiếp tục với phiên làm việc khác cho ta một danh sách khác mà ta có thể dùng để đối chiếu tìm `h`.
# - Vấn đề cuối cùng là tìm `m` thỏa `m+r*h=c (mod p)` với `h`, `c`, `p` đã biết khi tiến hành _submit_. Do khoảng giá trị của `m`, `r` là tương đối lớn (gần `10^12` trường hợp) nên việc vét cạn là không khả thi. Để ý biến đổi phương trình trên một chút, ta được: `m+r*h=c+k*p` hay `c+k*p=m (mod h)`.Trong trường hợp này, vét cạn `k` để tìm `m` thỏa `10^10 < m < 10^12` sẽ dễ dàng hơn.
# 
# #### Thực hiện
# **_B1:_** Kết nối đến server
# (Thư viện _mylib.py_ được đính kèm ở cuối bài viết.)

# In[1]:


from mylib import *
setup('random2win.acebear.site', 33337)
connect()


# **_B2:_** Chọn `m1=10^121`, `m2=0`. Gửi các giá trị lên server và nhận về `c1`, `c2` tương ứng.
# (Do `0 <= c1,c2 < p` nên `-p < (c1-c2) < p`, điều này đảm bảo `(m1-m2)-(c1-c2) > 10^121-p > 0`.)

# In[2]:


m1 = 10 ** 121
m2 = 0

send('1\n')
recvUntil('Message:') #đồng bộ với server
send(long_to_bytes(m1))
c1 = int(recvUntil('[0-9]{2,}')[0]) #tìm số có ít nhất 2 chữ số thập phân trong dữ liệu nhận về
send(long_to_bytes(m2))
c2 = int(recvUntil('[0-9]{2,}')[0])

print 'm1 = {}'.format(m1)
print 'm2 = {}'.format(m2)
print 'c1 = {}'.format(c1)
print 'c2 = {}'.format(c2)


# **_B3:_** Tính `d = (m1-m2)-(c1-c2)`. Biết `d` chia hết cho `p`, suy ra `p`. Với cách chọn `m1`, `m2` như trên, nếu để ý, ta sẽ thấy tỉ số `d/p < 11`

# In[3]:


d = (m1-m2) - (c1-c2)
print 'd = {}'.format(d)
print 'Số chữ số thập phân của d: {}'.format(len(str(d)))
for i in range(11,1,-1):
    if d%i == 0:
        p = d/i
        break
print 'p = {}'.format(p)
print 'Số chữ số thập phân của p: {}'.format(len(str(p)))


# **_B4:_** Tính danh sách `l1` gồm các giá trị có thể nhận của `h`. Thực hiện một kết nối khác đến server và tương tự tính danh sách `l2`, lấy tập giao gán lại cho `l1`: `l1 = l1 & l2` và lặp lại cho đến khi kích thước `l1 = 1`.

# In[4]:


l1 = [((c1-m1) * inverse(i,p)) % p for i in range(1,222222)] #Dùng cặp c2, m2 cũng cho kết quả tương tự

while True:
    connect()
    send('1\n')
    recvUntil('Message:') #đồng bộ với server
    send(long_to_bytes(m1))
    c1 = int(recvUntil('[0-9]{2,}')[0])
    l2 = [((c1-m1) * inverse(i,p)) % p for i in range(1,222222)]
    l1 = list(set(l1) & set(l2))
    print 'Kích cỡ tập giao: {}'.format(len(l1))
    if len(l1) == 1:
        h = l1[0]
        break

print 'h = {}'.format(h)


# **_B5:_** Kết nối đến server và chọn mục _Test_ để nhận `c`. Vét cạn `k` trong công thức `c+k*p = m (mod h)` cho đến khi được `10^10 < m < 10^12`. Cũng cần chú ý rằng, vì `m < 10^12 << h` nên xác suất `m` ngẫu nhiên nhỏ hơn `10^12` là rất thấp. Cũng có thể giới hạn `k` thông qua công thức `m + r*h = c + k*p`.

# In[5]:


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
