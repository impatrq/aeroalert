try:
    import usocket as socket
except:
    import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import random
import time
import json


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




def escuchar_tipos():
    conn, addr = s.accept()
    print('Got a type connection from %s' % str(addr))
    message = conn.recv(1024)
    
    tipo = json.loads(message.decode('utf-8'))
    
    if tipo == "soy_band":
        #iniciar thread para band
        escuchar_pulsera(conn, addr)
    elif tipo == "soy_rtdc":
        #iniciar thread para rtdc
        escuchar_rtdc(conn, addr)
        
        
        
def escuchar_rtdc(conn_rtdc,addr):
    message = conn_rtdc.recv(1024)
    print('Got a connection from rtdc %s' % str(addr))
    data = json.loads(message.decode('utf-8'))
    
    
def escuchar_band(conn_band, addr):
    
    message = conn_band.recv(1024)
    print('Got a connection from band %s' % str(addr))
    
    data = json.loads(message.decode('utf-8'))  #.decode('utf-8')
    bpm = data['1']
    spo = data['2']
    temp = data['3']

    print(data)
    
    print("bpm={:02} spo= {:02}% Temp {:02}°C".format(bpm, spo, temp))
    
while True:
    escuchar_tipos(conn, addr)
    
    
    escuchar_pulsera(conn, addr)

#para enviar datos
"""
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    response = web_page()
    conn.send(response)
    conn.close()
"""



#alternativa para recibir datos en vez de enviar
#aca recibiria lo de "some dummy content"


#para rtdc
"""
    #recibir datos
    response = ap_socket.recv(1024)
    print('Datos recibidos del ESP32 como Access Point:', response.decode(utf-8))
    
    
"""