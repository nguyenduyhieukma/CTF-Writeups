from aes_basics import aes_enc
import typing

block = bytes
state = typing.List[block]

def _xor(a: bytes, b:bytes) -> bytes:
  assert len(a) == len(b)
  return bytes(x ^ y for x, y in zip(a, b))

def _and(a: bytes, b:bytes) -> bytes:
  assert len(a) == len(b)
  return bytes(x & y for x, y in zip(a, b))

class Aegis128:
  const_0 = bytes.fromhex("000101020305080d1522375990e97962")
  const_1 = bytes.fromhex("db3d18556dc22ff12011314273b528dd")

  def __init__(self, key: bytes, tagsize :int = None):
    if len(key) != 16:
      raise ValueError("Invalid key length")
    self.key = key
    if tagsize not in [None, 16]:
      raise ValueError("Tag size not supported")
    self.tagsize = 16

  @staticmethod
  def state_update(S: state, m: bytes):
    S = [aes_enc(S[i - 1], S[i]) for i in range(len(S))]
    S[0] = _xor(S[0], m)
    return S

  def initialize(self, iv: block) -> state:
    k_iv = _xor(self.key, iv)
    S = [k_iv,
         self.const_1,
         self.const_0,
         _xor(self.key, self.const_0),
         _xor(self.key, self.const_1)]
    for _ in range(5):
      S = self.state_update(S, self.key)
      S = self.state_update(S, k_iv)
    return S

  @staticmethod
  def update_aad(S: state, aad: bytes) -> state:
    for i in range(0, len(aad), 16):
      adi = aad[i:i+16]
      if len(adi) < 16:
        adi += bytes(16 - len(adi))
      S = Aegis128.state_update(S, adi)
    return S

  @staticmethod
  def finalize(S: state, ad_bits, msg_bits) -> block:
    tmp = bytearray(S[3])
    for i in range(8):
      ad_bits, r = divmod(ad_bits, 256)
      tmp[i] ^= r
      msg_bits, r = divmod(msg_bits, 256)
      tmp[8 + i] ^= r
    for _ in range(7):
      S = Aegis128.state_update(S, tmp)
    tag = S[0]
    for r in S[1:5]:
      tag = _xor(tag, r)
    return tag

  @staticmethod
  def output_mask(S: state) -> block:
    tmp = _and(S[2], S[3])
    tmp = _xor(S[1], tmp)
    return _xor(S[4], tmp)

  @staticmethod
  def raw_encrypt(S: state, msg: bytes) -> typing.Tuple[state, bytes]:
    ct_blocks = []
    for i in range(0, len(msg), 16):
      blk = msg[i:i+16]
      mask = Aegis128.output_mask(S)
      if len(blk) < 16:
        mask = mask[:len(blk)]
        p = blk + bytes(16 - len(blk))
      else:
        p = blk
      ct_blocks.append(_xor(mask, blk))
      S = Aegis128.state_update(S, p)
    return S, b''.join(ct_blocks)

  def raw_decrypt(self, S: state, ct: bytes) -> typing.Tuple[state, bytes]:
    pt_blocks = []
    for i in range(0, len(ct), 16):
      blk = ct[i:i+16]
      mask = self.output_mask(S)
      p = _xor(mask[:len(blk)], blk)
      pt_blocks.append(p)
      if len(p) < 16:
        p += bytes(16 - len(blk))
      S = self.state_update(S, p)
    return S, b''.join(pt_blocks)

  def encrypt(self, iv: block, ad: bytes,
              msg: bytes) -> typing.Tuple[bytes, bytes]:
    S = self.initialize(iv)
    S = self.update_aad(S, ad)
    S, ct = self.raw_encrypt(S, msg)
    tag = self.finalize(S, len(ad) * 8, len(msg) * 8)
    return ct, tag

  def decrypt(self, iv: bytes, ad: bytes, ct: bytes, tag: bytes) -> bytes:
    S = self.initialize(iv)
    S = self.update_aad(S, ad)
    S, pt = self.raw_decrypt(S, ct)
    tag2 = self.finalize(S, len(ad) * 8, len(ct) * 8)
    if tag2 != tag:
      raise Exception('Invalid tag')
    return pt

class Aegis128L:
  const_0 = bytes.fromhex("000101020305080d1522375990e97962")
  const_1 = bytes.fromhex("db3d18556dc22ff12011314273b528dd")

  def __init__(self, key: bytes, tagsize:int = 16):
    if len(key) != 16:
      raise ValueError("Invalid key length")
    self.key = key
    if tagsize not in [None, 16]:
      raise ValueError("Tag size not supported")

    self.tagsize = 16

  @staticmethod
  def state_update(S, ma: bytes, mb: bytes):
    S = [aes_enc(S[i - 1], S[i]) for i in range(len(S))]
    S[0] = _xor(S[0], ma)
    S[4] = _xor(S[4], mb)
    return S

  def initialize(self, iv: block):
    k_iv = _xor(self.key, iv)
    S = [k_iv,
         self.const_1,
         self.const_0,
         self.const_1,
         k_iv,
         _xor(self.key, self.const_0),
         _xor(self.key, self.const_1),
         _xor(self.key, self.const_0)]
    for _ in range(10):
      S = self.state_update(S, iv, self.key)
    return S

  @staticmethod
  def update_aad(S, aad: bytes):
    for i in range(0, len(aad), 32):
      adi = aad[i:i+32]
      if len(adi) < 32:
        adi += bytes(32 - len(adi))
      S = Aegis128L.state_update(S, adi[:16], adi[16:])
    return S

  @staticmethod
  def finalize(S, ad_bits, msg_bits):
    tmp = bytearray(S[2])
    for i in range(8):
      ad_bits, r = divmod(ad_bits, 256)
      tmp[i] ^= r
      msg_bits, r = divmod(msg_bits, 256)
      tmp[8 + i] ^= r
    for _ in range(7):
      S = Aegis128L.state_update(S, tmp, tmp)
    # https://eprint.iacr.org/2013/695.pdf computes the tag as sum over S[0] .. S[7]
    # http://competitions.cr.yp.to/round1/aegisv1.pdf computes the tag as sum over S[0] .. S[6]
    tag = S[0]
    for r in S[1:7]:
      tag = _xor(tag, r)
    return tag

  @staticmethod
  def output_mask(S):
    tmp = _and(S[2], S[3])
    tmp = _xor(S[1], tmp)
    tmp = _xor(S[6], tmp)
    tmp2 = _and(S[6], S[7])
    tmp2 = _xor(S[5], tmp2)
    tmp2 = _xor(S[2], tmp2)
    return tmp + tmp2

  @staticmethod
  def raw_encrypt(S, msg: bytes):
    ct_blocks = []
    for i in range(0, len(msg), 32):
      blk = msg[i:i+32]
      mask = Aegis128L.output_mask(S)
      if len(blk) < 32:
        mask = mask[:len(blk)]
        p = blk + bytes(32 - len(blk))
      else:
        p = blk
      ct_blocks.append(_xor(mask, blk))
      S = Aegis128L.state_update(S, p[:16], p[16:])
    return S, b''.join(ct_blocks)

  def encrypt(self, iv: bytes, ad: bytes, msg: bytes):
    S = self.initialize(iv)
    S = self.update_aad(S, ad)
    S, ct = self.raw_encrypt(S, msg)
    tag = self.finalize(S, len(ad) * 8, len(msg) * 8)
    return ct, tag

