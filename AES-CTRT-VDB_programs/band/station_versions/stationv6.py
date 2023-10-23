import socket
import time
import urequests as requests
import random
import json


addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]
server_ip = '192.168.4.1'
server_port = 8000

def do_connect():
    import network
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
    return client_socket

def send_message(bpm, spo2, temp, client_socket):
    
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((server_ip, server_port))
    
    data = {'1': bpm, '2': spo2, '3': temp}
    message = json.dumps(data).encode('utf-8') #.encode('utf-8') para un string se encodea
    
    client_socket.send(message) 
    print('Mensaje enviado:', message)

    
    #respuesta = client_socket.recv(1024)
    #print('respuesta: ', respuesta)
    
    client_socket.close()
