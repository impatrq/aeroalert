from wireless import Wireless
import socket, json

def do_connect():
    ssid = 'ESP32'
    password = 'aeroalert'
    wire = Wireless()
    wire.connect(ssid, password)
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

def send_message(client_socket, data):
    
    # data = {"Piloto": 1,
    # "Somnolencia": 1,
    # "Pulso": 94,
    # "Spo2": 92,
    # "bloqueo": 1,
    # "Muerte": 1}
    message = json.dumps(data).encode('utf-8') #.encode('utf-8') para un string se encodea
    
    client_socket.send(message) 
    print('enviado:', message)

def receive_data(client_socket):
    data = client_socket.recv(1024)
    print('recibido: ', data)
    instruccion = json.loads(data.decode('utf-8'))

    return instruccion

