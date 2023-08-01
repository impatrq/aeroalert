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

def web_page():
    html = """hola roca %.2f""" % (random.randint(1,100))
    return html

addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]

ssid = 'ESP32'
password = '123456789'

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
s.listen(5)
print("listening on",addr)

"""
#para enviar datos
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    response = web_page()
    conn.send(response)
    conn.close()
"""
#alternativa para recibir datos en vez de enviar
#aca recibiria lo de "some dummy content"
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    time.sleep(0.1)
conn.close
