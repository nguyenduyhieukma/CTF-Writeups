import struct
from typing import List

# NOTE: NOTE: NOTE: This file contains a resonably fast implementation of
# the https://www.felixcloutier.com/x86/aesenc primitive so you can run the
# challenge. There's really nothing here, don't waste your time.

uint32 = int  # a 32-bit unsigned integer
uint8 = int  # a 8-bit unsigned integer
block = bytes  # a block of 16 bytes

def _xor(a: block, b:block) -> block:
  return bytes(x^y for x, y in zip(a, b))

sbox0 = bytes.fromhex(
    "637c777bf26b6fc53001672bfed7ab76"
    "ca82c97dfa5947f0add4a2af9ca472c0"
    "b7fd9326363ff7cc34a5e5f171d83115"
    "04c723c31896059a071280e2eb27b275"
    "09832c1a1b6e5aa0523bd6b329e32f84"
    "53d100ed20fcb15b6acbbe394a4c58cf"
    "d0efaafb434d338545f9027f503c9fa8"
    "51a3408f929d38f5bcb6da2110fff3d2"
    "cd0c13ec5f974417c4a77e3d645d1973"
    "60814fdc222a908846eeb814de5e0bdb"
    "e0323a0a4906245cc2d3ac629195e479"
    "e7c8376d8dd54ea96c56f4ea657aae08"
    "ba78252e1ca6b4c6e8dd741f4bbd8b8a"
    "703eb5664803f60e613557b986c11d9e"
    "e1f8981169d98e949b1e87e9ce5528df"
    "8ca1890dbfe6426841992d0fb054bb16")

def mod_poly(x: int) -> int:
  while x >= 256:
    r, x = divmod(x, 256)
    x ^= r ^ (r << 1) ^ (r << 3) ^ (r << 4)
  return x

def _rot8(x: uint32) -> uint32:
  return (x >> 8) | ((x & 0xff) << 24)

def mix_columns(b: bytes) -> bytes:
  """Applies the MixColumns step to 4 bytes."""
  if len(b) != 4:
    raise ValueError("expected 4 byte input")
  res = bytearray(4)
  for i in range(4):
    s = b[i]
    s2 = mod_poly(s << 1)
    s3 = s ^ s2
    res[i] ^= s2
    res[(i + 1) % 4] ^= s
    res[(i + 2) % 4] ^= s
    res[(i + 3) % 4] ^= s3
  return bytes(res)

te0 = [None] * 256
for i,s in enumerate(sbox0):
  t = mix_columns(bytes([s, 0, 0, 0]))
  te0[i] = struct.unpack(">I", t)[0]
te1 = [_rot8(x) for x in te0]
te2 = [_rot8(x) for x in te1]
te3 = [_rot8(x) for x in te2]

def _block_from_ints(v: List[uint32]) -> block:
  """Converts 4 integers into a block using bigendian order"""
  return struct.pack(">IIII", *v)

def aes_enc(s: block, round_key: block) -> block:
  """Performs the AESENC operation with tables."""
  t0 = (te0[s[0]] ^ te1[s[5]] ^ te2[s[10]] ^ te3[s[15]])
  t1 = (te0[s[4]] ^ te1[s[9]] ^ te2[s[14]] ^ te3[s[3]])
  t2 = (te0[s[8]] ^ te1[s[13]] ^ te2[s[2]] ^ te3[s[7]])
  t3 = (te0[s[12]] ^ te1[s[1]] ^ te2[s[6]] ^ te3[s[11]])
  s = _block_from_ints([t0, t1, t2, t3])
  return _xor(s, round_key)

