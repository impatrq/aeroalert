import network
import socket

def conectar_wifi():
    global s, ap
    # Configuracion
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
    return s, ap.ifconfig
    #s = socket
    #ap = access point