import struct
import socket
import struct
from itertools import chain

class UDPSocket ():

    def __init__(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.localIP     = "192.168.111.194"
        self.localPort   = 8000
        self.bufferSize  = 1024

    def loop(self):

        self.socket.listen()
        self.socket.bind((self.localIP, self.localPort))
        client, client_addr = self.socket.accept()
        print("Server listening")

    def udp_cliente(self, IP, port, message):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print (message)
        sock.sendto(message, (IP, port))

    def DREF (self, message, value):
        buf = bytearray(509)
        buf [0:3] = bytes('DREF', 'ascii')
        buf [5:8] = bytearray(struct.pack("f", value))
        buf[9:(9+len(message))] = bytes(message, 'ascii')
        return buf 
    
    def CMND (self, message):
        buf = bytearray()
        buf [0:3] = bytes('CMND', 'ascii')
        buf [5:(len(message))] = bytes(message, 'ascii')
        return buf
    
    def RREF (self, message, ID, frequency):
        buf = bytearray(413)
        buf [0:3] = bytes('RREF', 'ascii')
        buf [5:9] = bytearray(struct.pack("f", frequency))
        buf [9:13] = bytearray(struct.pack("f", ID))
        buf [13:(14+len(message))] = bytes(message, 'ascii')
        return buf
        

s = UDPSocket()
a = s.DREF('sim/cockpit/electrical/night_vision_on', 1.0)
s.udp_cliente('127.0.0.1', 49000, a)