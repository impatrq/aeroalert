from wireless import Wireless
import socket, json

# Conectarse a la red wifi llamada "ESP32" contraseña: "aeroalert"
def do_connect():     
    """
    ssid = 'ESP32'
    password = 'aeroalert'
    wire = Wireless()
    wire.connect(ssid, password)
    """
    server_ip = '192.168.4.1'
    server_port = 8000
    addr = socket.getaddrinfo(server_ip, server_port) [0][-1]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("conectado al aes")
    return client_socket
    
def send_type(tipo, client_socket):
    message = json.dumps(tipo).encode('utf-8')
    client_socket.send(message)

def send_message(client_socket, data):
    try:
        message = json.dumps(data).encode('utf-8')
        client_socket.send(message) 
        print('enviado:', message)
    except Exception as error:
        print(f"error: {error} \n {data}")
"""
def receive_data(client_socket):
    data = client_socket.recv(1024)
    print('recibido: ', data)
    return data 

"""