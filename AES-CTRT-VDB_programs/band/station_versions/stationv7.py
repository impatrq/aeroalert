import socket
import time
import urequests as requests
import random
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
    

def send_message(bpm, spo2, temp, client_socket, sta_if):
    
    data = {'1': bpm, '2': spo2, '3': temp}
    message = json.dumps(data).encode('utf-8') #.encode('utf-8') para un string se encodea
    
    print("owo")
    client_socket.send(message)
    print('Mensaje enviado:', message)

def send_type(tipo, client_socket, sta_if):
    
    message = json.dumps(tipo).encode('utf-8')
    client_socket.send(message)




client_socket, sta_if = do_connect()    
send_type("soy_band", client_socket, sta_if)
while True:
    time.sleep(1)
    send_message(123, 456, 789, client_socket, sta_if)
