try:
    import usocket as socket
except:
    import socket
import esp
esp.osdebug(None)
import time, json, _thread
import machine, network
from machine import Timer

pin_flag = machine.Pin(25, machine.Pin.OUT)

def conectar_wifi():
    global s, ap
    print("holawifi")
    #configuracion
    addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]
    ssid = 'ESP32'
    password = 'aeroalert'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    ap.config(authmode=3)
    while ap.active() == False:
        pass

    print('Connection succesful')
    print(ap.ifconfig())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.bind(('', 8000)) #o addr
    s.listen(2)
    print("listening on",addr)
    
    return s


def escuchar_rtdc(conn_rtdc, addr):
    pin_flag.value(0)
    try:
        while True:
            data = conn_rtdc.recv(1024)
            print('Got a connection from rtdc %s' % str(addr))
            message = json.loads(data.decode('utf-8'))
            print(message)

            # {'mensage': "aterriza"}
            if message['mensage'] == "aterriza":
                print("tiene que aterrizar")                        #ATERRIZAR ATERRIZAR ATERRIZAR ATERRIZAR ATERRIZAR ATERRIZAR                                             
                #enviar por wifi a PC y bloquear

    except:
        pin_flag.value(1)

s = conectar_wifi()

while True:
    print("Escuchando tipos")
    conn, addr = s.accept()
    print('Got a type connection from %s' % str(addr))
    message = conn.recv(1024)
    tipo = json.loads(message.decode('utf-8'))
    if tipo == "soy_rtdc":
        _thread.start_new_thread(escuchar_rtdc, (conn, addr))
        print("thread iniciado")






