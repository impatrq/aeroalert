from wireless import Wireless
import socket, json


ssid = 'ESP32'
password = 'aeroalert'

wire = Wireless()
wire.connect(ssid, password)

def do_connect():
    server_ip = '192.168.4.1'
    server_port = 8000
    addr = socket.getaddrinfo(server_ip, server_port) [0][-1]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("conecto")
    
    return client_socket
    
def send_type(tipo, client_socket):
    message = json.dumps(tipo).encode('utf-8')
    client_socket.send(message)

def send_message(client_socket,msg):
    data = {'mensage': msg}
    message = json.dumps(data).encode('utf-8') #.encode('utf-8') para un string se encodea
    
    client_socket.send(message) 
    print('Mensaje enviado:', message)

def receive_data(client_socket):
    data = client_socket.recv(1024)
    print('respuesta: ', data)
    return data


client_socket = do_connect()
send_type('soy_PC', client_socket)
send_message(client_socket, 'holiwis')
receive_data(client_socket)
