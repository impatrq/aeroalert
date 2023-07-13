import pulsometro
from pulsometro import Pulso
from machine import Timer
import _thread
import utime
import gc
gc.collect()

import stationv5 as station #se va a ir cambiando el nombre, cuidado

#creo objecto clase pulso
sensorsito = Pulso()

def mediciones():
    sensorsito.muestra()     #hace las mediciones

client_socket = 1
def mostrar():
    #crea un timer
    temporiza = Timer(0)
    global client_socket
    client_socket = station.do_connect()
    print(client_socket)
    #genera un desborde cada vez que el timer alcanza 350 llamando a la funcion "desborde"
    #temporiza.init(period=10000,mode=Timer.PERIODIC,callback=enviar)
    tinicial = utime.ticks_ms()
    while True:
        print(utime.ticks_ms() - tinicial)
        #asigna valores de las mediciones a las variables
        beats = sensorsito.datos
        spo2 = sensorsito.datos2
        temp = sensorsito.datos3
        gc.collect()
        print(gc.mem_free())
        #imprime las variables
        print(beats, spo2, temp) #"bpm={:02} SpO2= {:02}% Temp {:02}°C".format
        
        #try:
        station.send_message(beats, spo2, temp, client_socket)
        print("unu")
        """
        except Exception as why:
            if why.errno == 113:
                print("113", why)
                
                try:                    
                    client_socket = stationv5.socket_connect()
                except Exception as reason:
                    print("xd", reason)
                    
            elif why.errno == 9:
                print("9", why)
            else:
                print("no se", why)
            """
            
        utime.sleep(0.1)
    
#hago un thread para la funcion "mediciones"
_thread.start_new_thread(mediciones, ())

#hago un thread para la funcion "mostrar"
_thread.start_new_thread(mostrar, ())

"""
def enviar_wifi():
    stationv4.do_connect()
    while True:
        stationv4.send_message(1)
        time.sleep(3)
"""

