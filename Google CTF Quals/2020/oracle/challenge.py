import aegis
import base64
import secrets
import sys

flag = open('flag.txt').read().strip()


DATA = b"""
Hear your fate, O dwellers in Sparta of the wide spaces;

Either your famed, great town must be sacked by Perseus' sons,
Or, if that be not, the whole land of Lacedaemon
Shall mourn the death of a king of the house of Heracles,
For not the strength of lions or of bulls shall hold him,
Strength against strength; for he has the power of Zeus,
And will not be checked until one of these two he has consumed
"""

def runPhase1():
  print("Give me messages and I'll encrypt them for you.")
  key = secrets.token_bytes(16)
  iv = secrets.token_bytes(16)
  print(base64.b64encode(iv).decode("utf-8"))
  cipher = aegis.Aegis128L(key)
  for _ in range(7):
    pt = base64.b64decode(input().strip())
    aad = base64.b64decode(input().strip())
    ct, tag = cipher.encrypt(iv, aad, pt)
    print(base64.b64encode(ct).decode("utf-8"))
    print(base64.b64encode(tag).decode("utf-8"))
  state = base64.b64decode(input().strip())
  S2 = cipher.initialize(iv)
  S2 = cipher.state_update(S2, bytes(16), bytes(16))
  if state == b''.join(S2):
    print('OK')
  else:
    print('boo!')
    raise ValueError('Failed!')

def runPhase2():
  print("That was rude! I won't encrypt any messages anymore!")
  key = secrets.token_bytes(16)
  iv = secrets.token_bytes(16)
  aad = secrets.token_bytes(64)
  secret_plaintext = bytes(secrets.token_urlsafe(100), 'ascii')[:6*16]
  cipher = aegis.Aegis128(key)
  ct, tag = cipher.encrypt(iv, aad, secret_plaintext)
  print(base64.b64encode(iv).decode("utf-8"))
  print(base64.b64encode(aad).decode("utf-8"))
  print(base64.b64encode(ct).decode("utf-8"))
  print(base64.b64encode(tag).decode("utf-8"))
  for _ in range(231):
    try:
      msg = input().strip()
      if msg == "challenge":
        break
      ct = base64.b64decode(msg)
      S = cipher.initialize(iv)
      S = cipher.update_aad(S, aad)
      S, pt = cipher.raw_decrypt(S, ct)
      pt.decode("ascii")
      print('--OK--')
    except UnicodeDecodeError as ex:
      print(str(ex))
  ct = base64.b64decode(input().strip())
  aad = base64.b64decode(input().strip())
  tag = base64.b64decode(input().strip())
  if cipher.decrypt(iv, aad, ct, tag) == DATA:
    print(f"Congrats! Flag: {flag}")
  else:
    print("Fail")

if __name__ == '__main__':
  runPhase1()
  runPhase2()
