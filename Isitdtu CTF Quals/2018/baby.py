import os
import socket
import threading
from hashlib import *
import SocketServer
import random
from flag import flag
host, port = '0.0.0.0', 33337
BUFF_SIZE = 1024

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def hash(self, m):
        f = int(flag.encode("hex"),16)
        x = sha512(str(f | m )).digest().encode("hex")
        self.request.sendall(x+"\n")

        
        

    def check(self):
        while True:
            self.request.sendall("********************Hello World********************\n")
            self.request.sendall("***************************************************\n")
            self.request.sendall("Number: ")
            try:
                number = int(self.request.recv(BUFF_SIZE).strip())
            except:
                break
            self.request.sendall(str(number)+"\n")
            self.hash(number)
	   
    def handle(self):
        self.request.settimeout(1)        
        self.check()

    

def main():
	server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running in thread:", server_thread.name
	server_thread.join()

if __name__=='__main__':
    main()
