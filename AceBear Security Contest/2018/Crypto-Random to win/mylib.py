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
# Some useful functions from the PyCrypto package
######################################
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
