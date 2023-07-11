import pulsometro
from pulsometro import Pulso
from machine import Timer
import _thread
import utime

#import stationv5 as station #se va a ir cambiando el nombre, cuidado

#creo objecto clase pulso
sensorsito = Pulso()

def mediciones():
    sensorsito.muestra()     #hace las mediciones

client_socket = 1
def mostrar():
    #crea un timer
    #temporiza = Timer(0)
    #global client_socket
    #client_socket = station.do_connect()
    #print(client_socket)
    #genera un desborde cada vez que el timer alcanza 350 llamando a la funcion "desborde"
    #temporiza.init(period=10000,mode=Timer.PERIODIC,callback=enviar)
    while True:
        print()
        #asigna valores de las mediciones a las variables
        beats = sensorsito.datos
        spo2 = sensorsito.datos2
        temp = sensorsito.datos3
    
        #imprime las variables
        print(beats, spo2, temp) #"bpm={:02} SpO2= {:02}% Temp {:02}°C".format
        #station.send_message(beats, spo2, temp, client_socket)
        utime.sleep(5)
    
#hago un thread para la funcion "mediciones"
_thread.start_new_thread(mediciones, ())

#hago un thread para la funcion "mostrar"
_thread.start_new_thread(mostrar, ())

"""
def enviar (Timer):
    print()
    #asigna valores de las mediciones a las variables
    beats = sensorsito.datos
    spo2 = sensorsito.datos2
    temp = sensorsito.datos3
    
    global client_socket
    #imprime las variables
    print(beats, spo2, temp) #"bpm={:02} SpO2= {:02}% Temp {:02}°C".format
    stationv5.send_message(beats, spo2, temp, client_socket)
"""



"""
def enviar_wifi():
    station.do_connect()
    while True:
        station.send_message(1)
        utime.sleep(3)
"""