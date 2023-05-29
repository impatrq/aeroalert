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
"""
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    message = conn.recv(1024)
    
    data = json.loads(message.decode('utf-8'))  #.decode('utf-8')
    bpm = data['value1']
    spo2 = data['value2']
    temp = data['value3']
    
    print(data)
    
    print("bpm={:02} SpO2= {:02}% Temp {:02}°C".format(bpm, spo2, temp))
    
    respuesta = "hola"
    conn.send(respuesta)
    
    conn.close()
"""
#para enviar datos
"""
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    response = web_page()
    conn.send(response)
    conn.close()
"""


#para 2 stations y enviar data

#acepta las 2 conexiones y agarra los puertos
station1, addr1 = s.accept()
print('Conexión establecida con el ESP32 como estación 1(BAND):', addr1)
station2, addr2 = s.accept()
print('Conexión establecida con el ESP32 como estación 2(RTDC):', addr2)

def exchange_data(estacion1, estacion2):
    while True:
        message1 = estacion1.recv(1024)
        print("recibidos los del 1", message1)
        estacion1.send("uwu1")
        
        message2 = estacion2.recv(1024)
        print("recibidos los del 2", message2)
        estacion2.send("uwu2")
    """
        data1 = json.loads(message1.decode('utf-8'))
        bpm = data1['value1']
        spo2 = data1['value2']
        temp = data1['value3']
        print("bpm={:02} SpO2= {:02}% Temp {:02}°C".format(bpm, spo2, temp) )
    """
        

    """
        print('Datos recibidos:', message2.decode('utf-8'))
    """        
        # Enviar los mismos datos al otro ESP32 como estación
        #estacion2.sendall("uwu")
while True:
    exchange_data(station1, station2)

#alternativa para recibir datos en vez de enviar
#aca recibiria lo de "some dummy content"


#para rtdc
"""
    #recibir datos
    response = ap_socket.recv(1024)
    print('Datos recibidos del ESP32 como Access Point:', response.decode(utf-8))
    
    
"""