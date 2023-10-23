import struct
import socket
from socket import *
global i

class UDPSocket ():

    def __init__(self):
        self.socket = socket(AF_INET,SOCK_DGRAM)
        self.localIP     = "127.0.0.1"
        self.localPort   = 49004
        self.bufferSize  = 1024
        self.socket.bind((self.localIP, self.localPort))

    def loop(self):
        print("Server listening")

        #print("Before receiving data")
        bytesAddressPair = self.socket.recvfrom(self.bufferSize)
        #print("After receiving data")

        messages = bytesAddressPair[0]
        #address = bytesAddressPair[1]

        #print("Received message:", messages)
        #print("Source address:", address)
        return messages

    def udp_cliente(self, IP, port, message):

        sock = socket(AF_INET, SOCK_DGRAM)
        print (message)
        sock.sendto(message, (IP, port))

    def DREF (self, message, value):
        buf = bytearray(507)
        buf [0:3] = bytes('DREF', 'ascii')
        buf [5:8] = bytearray(struct.pack("f", value))
        buf[9:(9+len(message))] = bytes(message, 'ascii')
        return buf 
    
    def DREFtranslate (self, messages):
        hdgmode = "sim/cockpit2/autopilot/heading_mode"
        gpscourse = "sim/cockpit/radios/gps_course_degtm"
        navcourse = "sim/cockpit/radios/nav1_course_degm"
        maghdg = "sim/cockpit/autopilot/heading_mag"
        autostate = "sim/cockpit/autopilot/autopilot_mode"
        dme_dist = "sim/cockpit/radios/gps_dme_dist_m"
        vervel = "sim/cockpit/autopilot/vertical_velocity"
        preselvervel = "sim/cockpit2/autopilot/altitude_readout_preselector"
    
        if hdgmode in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [hdgmode, value]
        elif gpscourse in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [gpscourse, value]
        elif navcourse in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [navcourse, value]
        elif maghdg in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [maghdg, value]
        elif autostate in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [autostate, value]
        elif dme_dist in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [dme_dist, value]
        elif vervel in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [vervel, value]
        elif preselvervel in str(messages):
            buf = bytearray(messages)
            val = struct.unpack('f', buf [5:9])
            value = val[0]
            return [preselvervel, value]
        else:
            return None
            

    def CMND (self, message):
        buf = bytearray(5+len(message))
        buf [0:3] = bytes('CMND', 'ascii')
        buf [5:(5+len(message))] = bytes(message, 'ascii')
        return buf
    
    def RREF (self, message, ID, frequency):
        buf = bytearray(500)
        buf [0:3] = bytes('RREF', 'ascii')
        buf [5:9] = bytearray(struct.pack("f", frequency))
        buf [9:13] = bytearray(struct.pack("f", ID))
        buf [13:(13+len(message))] = bytes(message, 'ascii')

        return buf
    

#sim/autopilot/vertical_speed
#sim/cockpit2/autopilot/altitude_hold_status
    
#sim/GPS/g1000n1_hdg
#sim/autopilot/heading

#sim/autopilot/approach
#sim/GPS/g1000n1_apr

#sim/cockpit/radios/gps_dme_dist_m

'''a = s.CMND('sim/autopilot/approach')
s.udp_cliente('127.0.0.1', 49000, a)'''


print("UDP server up and listening")

# Listen for incoming datagrams
s = UDPSocket()
i = 1
while True:
    APST = 0
    APHDG = 0
    GPSCRS = 0
    NAVCRS = 0
    MHDG = 0
    DME = 0
    VARIO = 0
    PRESEL = 0
    hdgmode = "sim/cockpit2/autopilot/heading_mode"
    gpscourse = "sim/cockpit/radios/gps_course_degtm"
    navcourse = "sim/cockpit/radios/nav1_course_degm"
    maghdg = "sim/cockpit/autopilot/heading_mag"
    autostate = "sim/cockpit/autopilot/autopilot_mode"
    dme_dist = "sim/cockpit/radios/gps_dme_dist_m"
    vervel = "sim/cockpit/autopilot/vertical_velocity"
    preselvervel = "sim/cockpit2/autopilot/altitude_readout_preselector"
    a = s.loop()
    b = s.DREFtranslate(a)
    if hdgmode == b[0]:
        APHDG = int(b[1])
        #print(APHDG)
    elif gpscourse in b:
        GPSCRS = int(b[1])
        #print(GPSCRS)
    elif navcourse in b:
        NAVCRS = int(b[1])
        #print(NAVCRS)
    elif maghdg in b:
        MHDG = int(b[1])
        #print(MHDG)
    elif autostate in b:
        APST = int(b[1])
        #print(APST)
    elif dme_dist in b:
        DME = int(b[1])
        #print(APST)
    elif vervel in b:
        VARIO = int(b[1])
        #print(APST)
    elif preselvervel in b:
        PRESEL = int(b[1])
        #print(APST)
    if APST == 2:
        if i == 1:
            a = s.DREF('sim/cockpit2/autopilot/heading_mode', 1.0)
            g = s.DREF("sim/cockpit2/autopilot/heading_status", 2.0)
            f = s.CMND("sim/autopilot/vertical_speed")
            
            s.udp_cliente('127.0.0.1', 49000, a)
            s.udp_cliente('127.0.0.1', 49000, g)
            s.udp_cliente('127.0.0.1', 49000, f)
            if VARIO != 0:
                c = s.DREF("sim/cockpit/autopilot/vertical_velocity", PRESEL)
                s.udp_cliente("127.0.0.1", 49000, c)
            
            '''g = s.CMND("sim/autopilot/heading")
            s.udp_cliente("127.0.0.1", 49000, g)'''
            i = 2

        if NAVCRS - GPSCRS < 1 and DME < 6:
            if i == 2:
                '''a = s.CMND('sim/GPS/g1000n1_apr')
                s.udp_cliente('127.0.0.1', 49000, a)'''
                t = s.CMND("sim/autopilot/approach")
                s.udp_cliente('127.0.0.1', 49000, t)
                i = 3
