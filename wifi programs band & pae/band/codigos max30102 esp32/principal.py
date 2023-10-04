import pulsometro
from pulsometro import Pulso
from machine import Timer
from machine import Pin
import _thread
import utime
import gc
gc.collect()

import stationv9 as station #se va a ir cambiando el nombre, cuidado

#creo objecto clase pulso
sensorsito = Pulso()

client_socket = 1
pin_conectado = Pin(17, mode=Pin.IN)
pin_led = Pin(19, mode=Pin.OUT)
pin_prendido = Pin(16 , mode=Pin.IN)
conectado = pin_conectado.value()

led_prendido = 0
pin_prendido.value(1)



def mediciones():
    sensorsito.muestra(pin_prendido)     #hace las mediciones


def mostrar():
    utime.sleep(2)
    global client_socket
    if pin_prendido.value() == 1:

        print("intentando conectar")
        client_socket, sta_if = station.do_connect()    
        print(client_socket)

        station.send_type(client_socket, sta_if)
        while True:
            utime.sleep(3)
            while pin_prendido.value():
                
                if led_prendido == 0:
                    pin_led.value(1)
                    led_prendido = 1
                gc.collect()
                print(gc.mem_free())
                
                conectado = pin_conectado.value()
                beats = sensorsito.datos
                spo2 = sensorsito.datos2
                temp = sensorsito.datos3
                print("conectado: ", conectado)
                print(f'{beats}, {spo2}, {temp}')
                
                try:
                    #station.send_message(123, 456, 789, 1, client_socket, sta_if)
                    station.send_message(beats, spo2, temp, conectado, client_socket, sta_if)
                    print("enviado")
                except:
                    print("No enviado")

                utime.sleep(3)
            led_prendido = 0
            pin_led.value(0)
        

_thread.start_new_thread(mediciones, ())
utime.sleep(1)

_thread.start_new_thread(mostrar, ())



