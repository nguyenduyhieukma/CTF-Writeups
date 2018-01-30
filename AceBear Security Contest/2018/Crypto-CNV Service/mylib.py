from hashlib import md5
import socket
import re

######################################
# Socket wrapper functions
######################################
def setup(host,port):
    global _host, _port
    _host = host; _port = port
def disconnect():
    try: _sock.close()
    except: pass
def connect():
    global _sock
    disconnect()
    _sock = socket.socket()
    _sock.connect((_host,_port))
    _sock.settimeout(2)
def send(s): _sock.send(s)
def recv(silent=True):
	msg = _sock.recv(4096)
	if not silent: print msg
	return msg
def recvUntil(pattern, silent=True):
	while True:
		l = re.findall(pattern, recv(silent))
		if l: return l

######################################
# Reused functions from the challenge
######################################
def xor(dest, src):
    if len(dest) == 0:
        return src
    elif len(src) == 0:
        return dest
    elif len(dest) >= len(src):
        return ''.join(chr(ord(dest[i])^ord(src[i])) for i in range(len(src)))
    else:
        return ''.join(chr(ord(dest[i])^ord(src[i])) for i in range(len(dest)))
        
######################################
# MD5 hash wrapper function
######################################
def hash(s): return md5(s).digest()
