import socket
import time
import urequests as requests
import random
import json
import network

addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]
server_ip = '192.168.4.1'
server_port = 8000

def do_connect():
    global sta_if
    
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
    
    #"""----------------"""
    
    sta_if.active(False)
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
    print("conecto2")

    
    return client_socket
    

def send_message(bpm, spo2, temp, client_socket):
    global sta_if
    """
    print("antes")
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
    except Exception as why:
        print("no se", why)
    print("despues")
    """
    data = {'1': bpm, '2': spo2, '3': temp}
    message = json.dumps(data).encode('utf-8') #.encode('utf-8') para un string se encodea
    
    print("owo")
    client_socket.send(message)
    print('Mensaje enviado:', message)
    

    

    

    
    #respuesta = client_socket.recv(1024)
    #print('respuesta: ', respuesta)
    
    
