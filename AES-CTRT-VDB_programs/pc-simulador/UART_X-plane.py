import struct
import time
import _thread
import serial
from playsound import playsound

from socket import *
global i

# Se crea la clase UDPsocket, el cual se encarga de preparar y enviar los comandos al X-plane
class UDPSocket ():

    def _init_(self):
        self.socket = socket(AF_INET,SOCK_DGRAM)
        self.localIP     = "127.0.0.1"
        self.localPort   = 49004
        self.bufferSize  = 1024
        self.socket.bind((self.localIP, self.localPort))

    def loop(self):
        print("Server listening")

        bytesAddressPair = self.socket.recvfrom(self.bufferSize)

        messages = bytesAddressPair[0]
        return messages
    
    #Se establece una funcion para el evio de datos 
    def udp_cliente(self, IP, port, message):

        sock = socket(AF_INET, SOCK_DGRAM)
        sock.sendto(message, (IP, port))


    # Se establece funciones para la creacion de los distintos comandos para comunicarse con el X-Plane

    def DREF (self, message, value):
        buf = bytearray(507)
        buf [0:3] = bytes('DREF', 'ascii')
        buf [5:8] = bytearray(struct.pack("f", value))
        buf[9:(9+len(message))] = bytes(message, 'ascii')
        return buf 
    

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
    

    
global alarma_sonora_aes_activation, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_hypoxia, alarma_sonora_manual_activation, alarma_sonora_test_failed, alarma_sonora_test_pass

alarma_sonora_aes_activation = alarma_sonora_aes_alert = alarma_sonora_sleep = alarma_sonora_hypoxia = alarma_sonora_manual_activation = alarma_sonora_test_failed = alarma_sonora_test_pass = 0


def thread_sonidos():
    global alarma_sonora_aes_activation, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_hypoxia, alarma_sonora_manual_activation, alarma_sonora_test_failed, alarma_sonora_test_pass
    while True:
        #Comprobamos caules alertas estan activadas
        if alarma_sonora_aes_activation:
            playsound("./Sonidos/alerta_aes_act.mp3")     
        if alarma_sonora_aes_alert:
            playsound("./Sonidos/alerta_aes_alert.mp3")
        if alarma_sonora_sleep:
            playsound("./Sonidos/alerta_get_up.mp3")
        if alarma_sonora_hypoxia:
            playsound("./Sonidos/alerta_hypoxia.mp3")
        if alarma_sonora_manual_activation:
            playsound("./Sonidos/alerta_manual_act.mp3")
        if alarma_sonora_test_failed:
            playsound("./Sonidos/alerta_test_failed.mp3")
            alarma_sonora_test_failed = 0
        if alarma_sonora_test_pass:
            playsound("./Sonidos/alerta_test_pass.mp3")
            alarma_sonora_test_pass = 0

#Establecemos un Thread para la realizacion de las alertas mientras se lee la infomacion de UART
_thread.start_new_thread(thread_sonidos, ())


#se conecta al puerto serial
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    timeout=0
    )
print("connected to: " + ser.portstr)

lua_xplane = 0

def thread_xplane():
    global lua_xplane 
    j = 0
    while True:

        if lua_xplane:

            if j == 0:

                print("UDP server up and listening")

                s = UDPSocket()
                a = s.CMND('FlyWithLua/ViewPoint/Safe_Return')
                s.udp_cliente('127.0.0.1', 49000, a)

                j = j +1

        time.sleep(4)
_thread.start_new_thread(thread_xplane, ())

b = 1
i = 0

while True:
    #leemos la informacion enviada por la ESP32 
    leer = ser.readline()
    read = leer.decode('utf-8')
    if read:
        b = b+1
        print(read)

        #comprobamos que mensaje es
        if "aterrizar" in read:
            print("aterrizando")
            if i == 0:
                lua_xplane = 1
                i = i +1
        elif read == "no aterrizar":
            lua_xplane = 0
            print("desaterrizando")

        elif "[" in read and "]" in read:
            datos = list(read)
            if datos[0] == "info aeropuerto:":
                #xplane.instruccion(read[1])
                print("enviar info de aeropuerto", datos[0])

        #comprobamos si el mensaje es el que deberia ser 
        #----
        if "alarma_aes_activation=1" in read:
            alarma_sonora_aes_activation = 1
        elif "alarma_aes_activation=0" in read:
            alarma_sonora_aes_activation = 0
        #----
        elif "alarma_hipoxia=1" in read:
            alarma_sonora_hypoxia = 1
        elif "alarma_hipoxia=0" in read:
            alarma_sonora_hypoxia = 0
        #----
        elif "alarma_aes_alert=1" in read:
            alarma_sonora_aes_alert = 1
        elif "alarma_aes_alert=0" in read:
            alarma_sonora_aes_alert = 0
        #-----
        elif "alarma_dormidos=1" in read:
            alarma_sonora_sleep = 1
        elif "alarma_dormidos=0" in read:
            alarma_sonora_sleep = 0
        #----
        elif "alarma_manual_activation=1" in read:
            alarma_sonora_manual_activation = 1
        elif "alarma_manual_activation=0" in read:
            alarma_sonora_manual_activation = 0
        #----
        elif "alarma_test_failed" in read:
            alarma_sonora_test_failed = 1
        #----
        elif "alarma__test_pass" in read:
            alarma_sonora_test_pass = 1
        #----




