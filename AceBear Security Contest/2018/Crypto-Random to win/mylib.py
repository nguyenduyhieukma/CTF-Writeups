from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
import socket, re
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
    _sock.settimeout(1)
def send(s): _sock.send(s)
def recv(): return _sock.recv(4096)
def recvUntil(pattern):
	while True:
		l = re.findall(pattern, recv())
		if l: return l