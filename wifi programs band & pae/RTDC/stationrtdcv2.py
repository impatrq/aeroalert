import socket, json
import network, time

def do_connect():
    server_ip = '192.168.4.1'
    server_port = 8000
    addr = socket.getaddrinfo(server_ip, server_port) [0][-1]
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('ESP32','aeroalert')
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(.1)
        print()
    print('network config:', sta_if.ifconfig())
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("conecto")
    return client_socket, sta_if.ifconfig
    
def send_type(client_socket, tipo):
    message = json.dumps(tipo).encode('utf-8')
    client_socket.send(message)

def send_message(client_socket,msg):
    data = {'mensage': msg}
    message = json.dumps(data).encode('utf-8') 
    client_socket.send(message) 
    print('Mensaje enviado:', message)

def receive_data(client_socket):
    data = client_socket.recv(1024)
    info = json.loads(data.decode('utf-8'))
    print('respuesta: ', info)
    return info

