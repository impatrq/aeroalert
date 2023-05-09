import pulsometro
from pulsometro import Pulso
from machine import Timer
import _thread
import time

#creo objecto clase pulso
sensorsito = Pulso()

def mediciones():
    sensorsito.muestra()     #hace las mediciones

def desborde (Timer):
    print("*\n"*1)
    #asigna valores de las mediciones a las variables
    beats = sensorsito.datos
    spo2 = sensorsito.datos2
    temp = sensorsito.datos3
    #imprime las variables
    print("bpm={:02} SpO2= {:02}% Temp {:02}°C".format(beats, spo2, temp))

def mostrar():
    #crea un timer
    temporiza = Timer(0)
    #genera un desborde cada vez que el timer alcanza 350 llamando a la funcion "desborde"
    temporiza.init(period=350,mode=Timer.PERIODIC,callback=desborde)

#hago un thread para la funcion "mediciones"
_thread.start_new_thread(mediciones, ())
time.sleep(0.5)
#hago un thread para la funcion "mostrar"
_thread.start_new_thread(mostrar, ())
