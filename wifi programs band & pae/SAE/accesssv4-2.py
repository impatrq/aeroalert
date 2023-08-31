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
import _thread

#configuracion
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
    while True:
        conn, addr = s.accept()
        print('Got a type connection from %s' % str(addr))
        message = conn.recv(1024)
        
        tipo = json.loads(message.decode('utf-8'))
        
        if tipo == "soy_band":
            _thread.start_new_thread(escuchar_band, (conn, addr))
            #iniciar thread para band
            
        elif tipo == "soy_rtdc":
            #iniciar thread para rtdc
            escuchar_rtdc(conn, addr)
        
        
        
def escuchar_rtdc(conn_rtdc,addr):
    while True:
        message = conn_rtdc.recv(1024)
        print('Got a connection from rtdc %s' % str(addr))
        data = json.loads(message.decode('utf-8'))
    
    
def escuchar_band(conn_band, addr):
    while True:
    
        message = conn_band.recv(1024)
        print()
        print('Got a connection from band %s' % str(addr))
        try:
            data = json.loads(message.decode('utf-8'))  #.decode('utf-8')
            bpm = data['1']
            spo = data['2']
            temp = data['3']
            conectado = data['4']
            print(data)
            
            print("bpm={:02} spo= {:02}% Temp {:02}°C ...conectado= {:1}".format(bpm, spo, temp, conectado))
        except:
            print("no se pudo unu")
            time.sleep(1)
            break
while True:
    escuchar_tipos()


#para enviar datos
"""
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    response = web_page()
    conn.send(response)
    conn.close()
"""

#para rtdc
"""
    #recibir datos
    response = ap_socket.recv(1024)
    print('Datos recibidos del ESP32 como Access Point:', response.decode(utf-8))
    
    
"""