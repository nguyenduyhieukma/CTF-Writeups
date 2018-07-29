#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flag import flag,key

assert len(key) == 10

if len(flag) % len(key) != 0:
    n = len(key) - len(flag) % len(key)
    for i in range(n):
        flag += " "
m = []
for a in range(len(key)):
    i = a
    for b in range(len(flag)/len(key)):
        if b % 2 != 0:
            m.append(ord(flag[i]) ^ ord(key[a]))
        else:
            m.append(ord(flag[i+len(key)-(a+1+a)])^ ord(key[a]))
        i += len(key)
enc_flag = ""
for j in range(len(m)):
    enc_flag += "%02x" % m[j]

print enc_flag

#enc_flag = 1d14273b1c27274b1f10273b05380c295f5f0b03015e301b1b5a293d063c62333e383a20213439162e0037243a72731c22311c2d261727172d5c050b131c433113706b6047556b6b6b6b5f72045c371727173c2b1602503c3c0d3702241f6a78247b253d7a393f143e3224321b1d14090c03185e437a7a607b52566c6c5b6c034047
