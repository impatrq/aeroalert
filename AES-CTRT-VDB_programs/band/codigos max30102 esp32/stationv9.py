import socket
import time
import json
import network

def do_connect():
    addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]
    server_ip = '192.168.4.1'
    server_port = 8000
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('ESP32','aeroalert')
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(.1)
        print()
    print('network config:' , sta_if.ifconfig())
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("conecto")
    
    return client_socket, sta_if
    
def send_message(bpm, spo2, temp, conectado, client_socket, sta_if):
    
    data = {'1': bpm, '2': spo2, '3': temp, '4': conectado}
    message = json.dumps(data).encode('utf-8')        #.encode('utf-8') para un string se encodea

    client_socket.send(message)
    

def send_type(client_socket, sta_if):
    message = json.dumps('soy_band').encode('utf-8')
    client_socket.send(message)

