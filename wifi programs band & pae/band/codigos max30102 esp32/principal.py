import pulsometro
from pulsometro import Pulso
from machine import Timer
from machine import Pin
import _thread
import utime
import gc
gc.collect()

import stationv8 as station #se va a ir cambiando el nombre, cuidado

#creo objecto clase pulso
sensorsito = Pulso()
def mediciones():
    sensorsito.muestra()     #hace las mediciones

client_socket = 1
pin_conectado = Pin(17, mode=Pin.IN)
pin_led = Pin(19, mode=Pin.OUT, value=1)
conectado = pin_conectado.value()
def mostrar():

    #temporiza = Timer(0)
    utime.sleep(2)
    global client_socket
    print("intentando conectar")
    client_socket, sta_if = station.do_connect()    
    print(client_socket)

    station.send_type("soy_band", client_socket, sta_if)

    while True:
        print()
        gc.collect()
        print(gc.mem_free())
        
        conectado = pin_conectado.value()
        beats = sensorsito.datos
        spo2 = sensorsito.datos2
        temp = sensorsito.datos3
        print("conectado: ", conectado)
        print(beats, spo2, temp) #"bpm={:02} SpO2= {:02}% Temp {:02}°C".format
        
        try:
            #station.send_message(123, 456, 789, 1, client_socket, sta_if)
            station.send_message(beats, spo2, temp, conectado, client_socket, sta_if)
            print("enviado")
        except:
            print("No enviado")

        utime.sleep(3)
    

_thread.start_new_thread(mediciones, ())
utime.sleep(1)

_thread.start_new_thread(mostrar, ())



