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

from wifi_connection import connect_wifi

s = connect_wifi()

station1, addr1 = s.accept()
print('Conexión establecida con el ESP32 como estación 1(BAND):', addr1)
station2, addr2 = s.accept()
print('Conexión establecida con el ESP32 como estación 2(RTDC):', addr2)

def exchange_data(estacion1, estacion2):
    while True:
        message1 = estacion1.recv(1024)
        print("recibidos los del 1", message1)
        estacion1.send("uwu1")

        evaluar_info(message1)

        
        message2 = estacion2.recv(1024)
        print("recibidos los del 2", message2)
        estacion2.send("uwu2")

        """
        print('Datos recibidos:', message2.decode('utf-8'))
        """        

        
def evaluar_info(message):
    data1 = json.loads(message.decode('utf-8'))
    bpm = data1['value1']
    spo2 = data1['value2']
    temp = data1['value3']
    print("bpm={:02} SpO2= {:02}% Temp {:02}°C".format(bpm, spo2, temp))
    
    if bpm < 90:
        print("tas muerto /n")

while True:
    exchange_data(station1, station2)
