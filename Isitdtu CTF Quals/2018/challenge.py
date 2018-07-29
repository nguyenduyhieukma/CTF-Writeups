import os
import socket
import threading
import time
import SocketServer
from AES_CNV import Game
from Crypto import Random
from Secret import __FLAG__

host, port = '0.0.0.0', 13337
BUFF_SIZE = 1024

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(10)
        self.game = Game()
        self.request.sendall("******************************************************************\n")
        self.request.sendall("* Challenge created by chung96vn                                 *\n")
        self.request.sendall("* My blog: https://chung96vn.blogspot.com                        *\n")
        self.request.sendall("* From: AceBear Team                                             *\n")
        self.request.sendall("******************************************************************\n\n\n")
        self.request.sendall("Give me content of your request you want to encrypt: ")
        try:
            req = self.request.recv(BUFF_SIZE).strip()
        except:
            self.request.sendall("Error!\n")
            exit()
        if req.startswith("Give me the flag"):
            self.request.sendall("Sorry! We don't support it!\n")
            exit()
        self.request.sendall("Your encypted: ")
        self.request.sendall(self.game.encode(req)+"\n")
        self.request.sendall("Give me encrypted of your request: ")
        enc = self.request.recv(BUFF_SIZE).strip()
        try:
            dec = self.game.decode(enc)
        except:
            self.request.sendall("Error!\n")
            exit()
        self.request.sendall("Your request: %s\n" %dec)
        if dec.startswith("Give me the flag"):
            self.request.sendall("This is flag: %s\n" %__FLAG__)
        self.request.sendall("Bye~~")
                
def main():       
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    server_thread.join()

if __name__ == '__main__':
    main()