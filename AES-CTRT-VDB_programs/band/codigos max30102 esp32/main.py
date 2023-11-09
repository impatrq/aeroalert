import utime
utime.sleep(2)

from pulsometro import Pulso
from machine import Pin
import _thread, utime, gc
import stationv9 as station                                                                                               # Se va a ir cambiando el nombre, cuidado



sensor = Pulso()                                # Creo objecto clase pulso
pin_conectado = Pin(17, mode=Pin.IN)                                                                                        # pin_prendido.value(1)     porque es el boton y tiene 
pin_led = Pin(19, mode=Pin.OUT)                                                                                                     # que estar prendido para que ande
conectado = pin_conectado.value()
client_socket = 0
                                                                                    
def mediciones():
    sensor.muestra()     # Realiza las mediciones

def mostrar():
    utime.sleep(0.5)
    global client_socket
    while True:
        #if pin_prendido.value() == 0:
        print("intentando conectar al AES")
        client_socket, sta_if = station.do_connect()    
        print("conectado al AES", client_socket)
        station.send_type(client_socket, sta_if)

        while True:
            """
            while pin_prendido.value():
                if led_prendido == 0:
                    pin_led.value(1)
                    led_prendido = 1
                    """
            beats = sensor.datos
            spo2 = sensor.datos2
            temp = sensor.datos3
            conectado = 1 #pin_conectado.value()
            try:
                #if beats > 55 and beats < 140:
                station.send_message(beats, spo2, temp, 
                                     conectado, client_socket, sta_if)
                print("enviado")
                print('',beats,'', spo2,'', temp,'', conectado)
            except Exception as error:
                print("No enviado",error)
            gc.collect()
            utime.sleep(4)

        utime.sleep(3)
_thread.start_new_thread(mediciones,()) # Proceso paralelo que mide el sensor
utime.sleep(0.5)
_thread.start_new_thread(mostrar,()) #Proceso paralelo agarra valores y envia



