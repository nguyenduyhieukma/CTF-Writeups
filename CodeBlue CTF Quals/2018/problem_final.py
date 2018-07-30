# The LED block cipher implementation is based on the Jian Guo's reference implementation (http://led.crypto.sg/downloads/Reference-LED-ePrint.zip?attredirects=0&d=1)
# Written by Bono(Twitter ID: @Bono_iPad) for CODE BLUE CTF 2018 Qual

import os
from FLAG import FLAG

LED = 64

state = [[0 for i in range(4)] for j in range(4)]

MixColMatrix = [
	[4,  1, 2, 2],
	[8,  6, 5, 6],
	[11,14,10, 9],
	[2,  2,15,11],
]

sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
WORDFILTER = 0xF

sbox_lazy = [i for i in range(0,16)]

# For my safety, I use sbox_lazy for lazy encrypting!
while True:
  for a in range(20):
    q = ord(os.urandom(1)) % 16
    r = ord(os.urandom(1)) % 16
    sbox_lazy[q], sbox_lazy[r] = sbox_lazy[r], sbox_lazy[q]
  diff = 0
  for a in range(16):
    if sbox_lazy != a:
      diff += 1
  if diff > 6:
    break

def FieldMult(a,b):
  ReductionPoly = 0x3
  x = a
  ret = 0
  for i in range(0,4):
    if (b>>i)&1 == 1: ret ^= x
    if (x&0x8) != 0:
      x <<= 1
      x ^= ReductionPoly
    else: x <<= 1
  return ret&WORDFILTER

def AddKey(keyBytes,step):
  global state
  for i in range(0,4):
    for j in range(0,4):
      state[i][j] ^= keyBytes[(4*i+j+step*16)%(LED/4)]
  return state

def AddConstants(r):
  global state
  RC = [
		0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F,
		0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B,
		0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E,
		0x1C, 0x38, 0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A,
		0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04
	]
  state[1][0] ^= 1
  state[2][0] ^= 2
  state[3][0] ^= 3

  state[0][0] ^= (LED>>4)&0xf
  state[1][0] ^= (LED>>4)&0xf
  state[2][0] ^= LED & 0xf
  state[3][0] ^= LED & 0xf

  tmp = (RC[r] >> 3) & 7
  state[0][1] ^= tmp
  state[2][1] ^= tmp
  tmp =  RC[r] & 7
  state[1][1] ^= tmp
  state[3][1] ^= tmp


def SubCell():
  global state
  for i in range(0,4):
    for j in range(0,4):
      state[i][j] = sbox[state[i][j]]

def ShiftRow():
  global state
  tmp = [0]*4
  for i in range(1,4):
    for j in range(0,4):tmp[j] = state[i][j]
    for j in range(0,4):state[i][j] = tmp[(j+i)%4]

def MixColumn():
  global state
  tmp = [0]*4
  for j in range(0,4):
    for i in range(0,4):
      sum = 0
      for k in range(0,4):
        sum ^= FieldMult(MixColMatrix[i][k], state[k][j])
      tmp[i] = sum
    for i in range(0,4):state[i][j] = tmp[i]

def LED_enc(input,userkey,ksbits):
  global state, LED
  keyNibbles = [0]*32

  for i in range(0,16):
    if (i%2) == 1: state[i/4][i%4] = input[i>>1]&0xF
    else: state[i/4][i%4] = (input[i>>1]>>4)&0xF

  for i in range(0,ksbits/4):
    if (i%2) == 1: keyNibbles[i] = userkey[i>>1]&0xF
    else: keyNibbles[i] = (userkey[i>>1]>>4)&0xF

  LED = ksbits
  RN = 48
  if LED <= 64: RN = 32
  AddKey(keyNibbles,0)

  for i in range(0,RN/4):
    for j in range(0,4):
      AddConstants(i*4+j)
      SubCell()
      ShiftRow()
      MixColumn()
    AddKey(keyNibbles, i+1)

  output = [0]*8
  ret = ""
  for i in range(0,8):
    output[i] = ((state[(2*i)/4][(2*i)%4] & 0xF) << 4) | (state[(2*i+1)/4][(2*i+1)%4] & 0xF)
    ret += chr( output[i] )
 
  return ret

def Lazy_LED_enc(input,userkey,ksbits,rounds):
  global state, LED, sbox_lazy

  if rounds < 1 or rounds > 10:
    print "Sorry I'm not in the mood. Bye!"
    exit(0)

  keyNibbles = [0]*32

  for i in range(0,16):
    if (i%2) == 1: state[i/4][i%4] = input[i>>1]&0xF
    else: state[i/4][i%4] = (input[i>>1]>>4)&0xF

  for i in range(0,ksbits/4):
    if (i%2) == 1: keyNibbles[i] = userkey[i>>1]&0xF
    else: keyNibbles[i] = (userkey[i>>1]>>4)&0xF

  LED = ksbits
  RN = 48
  if LED <= 64: RN = 32
  AddKey(keyNibbles,0)

  rr = 0

  for i in range(0,RN/4): # I don't want to do it so many times!
    for j in range(0,4):
      AddConstants(i*4+j)
      SubCell()
      ShiftRow()
      MixColumn()
      rr += 1
      if rr == rounds:break # bye!
    if rr == rounds:break # bye!
    AddKey(keyNibbles, i+1)

  """  Making output string is so hard for me!
  output = [0]*8
  ret = ""
  for i in range(0,8):
    output[i] = ((state[(2*i)/4][(2*i)%4] & 0xF) << 4) | (state[(2*i+1)/4][(2*i+1)%4] & 0xF)
    ret += chr( output[i] )
  """
  ret = ""
  for i in range(0,4):
    for j in range(0,4):
      ret += chr(state[i][j])

  ret2 = ""
  for i in range(16):
    ret2 += ret[ sbox_lazy[i] ] # Now it's safe!

  return ret2

def main():
  print "Welcome to the LED encrypter!"
  K = os.urandom(16)
  for a in range(200):
   try:
    lazy = 0
    print "Please input your plaintext in hex."
    P = raw_input()
    if P == "exit":break
    if P[-5:-1] == "lazy":
      lazy = int(P[-1])
      print "Nice.", lazy
    P = P[0:16].decode("hex")

    k_data = []
    p_data = []
    for i in range( len(K) ):
      k_data.append( ord(K[i]) )
    for i in range( len(P) ):
      p_data.append( ord(P[i]) )

    print "plaintext: "
    print p_data
    print "ciphertext: "
    if lazy == 0:print LED_enc(p_data, k_data, len(K)*8).encode('hex')
    else: print Lazy_LED_enc(p_data, k_data, len(K)*8, lazy).encode('hex')
   except:
    print "Something wrong. Try again!"
    pass

  print "So, you got my key?"
  try:
   my_key = raw_input()[0:32].decode("hex")
   if K == my_key:
    print "Wow! You are awesome! Here is your flag!"
    print FLAG
   else:
    print "Nope, Bye!"
  except:
    print "Something wrong..."

if __name__ == '__main__':
  main()

