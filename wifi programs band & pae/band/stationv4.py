import socket
import time
import urequests as requests
import random
import json
addr = socket.getaddrinfo('192.168.4.1', 8000) [0][-1]

def numerito():
    num = random.randint(1,100)
    return num
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('ESP32','123456789')
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(.1)
        print()
    print('network config:' , sta_if.ifconfig())
    
def send_message(bpm, spo2, temp):
    server_ip = '192.168.4.1'
    server_port = 8000
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    data = {'value1': bpm, 'value2': spo2, 'value3': temp}
    message = json.dumps(data).encode('utf-8') #.encode('utf-8') para un string se encodea
    
    client_socket.send(message) 
    
    print('Mensaje enviado:', message)
    
    client_socket.close()
"""
do_connect()

while True:
    send_message()
    time.sleep(2)
    """
    
"""
#para recibir datos
while True:
    data = s.recv(1024)
    if data:
        print(data)
    else:
        break
s.close()
"""

#alternativa para enviar info en vez de recibir
#envia la info que quiero como una urequest a esa direccion
#response = requests.post("192.168.4.1", data = "some dummy content")
#print(response.txt)
#print(response.json())
"""
post_data = (a,b,c) = (1,3,5)
while True:
    resp = requests.post("192.168.4.1", data = post_data)
    #puedo poner "numerito"
    
    
    print(resp.txt)
    print(resp.json())
    time.sleep(0.1)
s.close()
"""    
