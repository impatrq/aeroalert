try:
    import usocket as socket
except:
    import socket
import network
import esp, gc
esp.osdebug(None)
gc.collect()
import random, json, time

from wifi_connection import connect_wifi

s = connect_wifi()

listabpm = []
listaspo2 = []

station1, addr1 = s.accept()
print('Conexión establecida con el ESP32 como estación 1(BAND):', addr1)
station2, addr2 = s.accept()
print('Conexión establecida con el ESP32 como estación 2(RTDC):', addr2)

def exchange_data(estacion1, estacion2):
    
    while True:
        message1 = estacion1.recv(1024)
        print("recibidos los del 1", message1)
        # en la pulsera los datos se envian cada 5 segs
        estacion1.send("uwu1")

        evaluar_info(message1)
        
        message2 = estacion2.recv(1024)
        print("recibidos los del 2", message2)  #borrar
        estacion2.send("uwu2")

        """
        print('Datos recibidos:', message2.decode('utf-8'))
        """
        
        
        
# Configurar los pines de la luz y el botón
pin_luz_bpm = machine.Pin(5, machine.Pin.OUT)
pin_boton = machine.Pin(4, machine.Pin.IN)
pin_luz_spo2 = machine.Pin(6, machine.Pin.OUT)

# Función para la desactivación del PAE
def desactivar_PAE(luz):
    print("PAE desactivado") #borrar
    
    if luz == "bpm":
        pin_luz_bpm.value(0) #resto de alertas luz amarilla
    elif luz == "spo2":
        pin_luz_spo2.value(0) #unica alerta con luz roja
    elif luz == "tocoboton":
        pin_luz_spo2.value(0) #apaga las 2 alertas
        pin_luz_bpm.value(0)
        
# Función para la activación del PAE
def activar_PAE(tipo):
    print("Emergencia") #borrar
    
    tiempo_inicial = utime.ticks_ms()  # Obtiene el tiempo inicial en milisegundos
    tiempo_objetivo = 9000  # 1 minuto y medio en milisegundos
    while utime.ticks_diff(utime.ticks_ms(), tiempo_inicial) < tiempo_objetivo:
        if pin_boton.value() == 1:
            desactivar_PAE("tocoboton") #pudo tocar el boton de reaccion
            break
    if pin_boton.value() == 1:
        break


        
    if tipo == "hipocardia":
        pin_luz_bpm.value(1)
        return("este mensaje significa que el piloto tiene hipocardia")
    elif tipo == "hipercardia":
        pin_luz_bpm.value(1)
        return("este mensaje significa que el piloto tiene hipercardia")
   
    elif tipo == "hipoxia":
        pin_luz_spo2.value(1)
        return(" hipoxia")
    
    elif tipo == "dormido":
        pin_luz_bpm.value(1)
        return("este mensaje significa que el piloto esta dormido")
        
def evaluar_info(message):
    data1 = json.loads(message.decode('utf-8'))
    bpm = data1['value1']
    spo2 = data1['value2']
    temp = data1['value3']
    print("bpm={:02} SpO2= {:02}% Temp {:02}°C".format(bpm, spo2, temp))  #borrar
    
    listabpm.append(bpm)
    listabpm = listabpm[-12:]
    listaspo2.append(spo2)
    listaspo2 = listaspo2[-12:] #12 valores cada uno 5 segs despues son 60 segs en total
    
    print(listabpm)  #borrar
    # Evaluar el valor de pulsaciones y activar/desactivar el PAE según corresponda
    if bpm < 50:
        print("tas muerto unu /n")  #borrar
        msgalerta = activar_PAE(hipocardia)
        return (msgalerta)
    elif bpm > 140:
        print("tas muerto -~- /n")  #borrar
        msgalerta = activar_PAE(hipercardia)
        return (msgalerta)
        # paro cardiaco si es que estas descansando, pueden llegar a aumentar por sobre eso si esta nervioso o algo asi
        # si es por mas de 20 segundos puede ser un paro cardiaco4
        # mas de 150 taquicardia ventricular durante un minuto
    else:
        desactivar_PAE()   
    
    
    # Evaluar el valor de oxígeno en sangre y activar/desactivar el PAE según corresponda
    if spo2 <= 90:
        activar_PAE(spo2)
    elif spo2 > 90:
        desactivar_PAE(spo2)
    
        
    #segun temperaturas:
    if temp < 5:
        #se esta congelando
    elif temp > 40:
        #esta ardiendo casi el sensor
        
    if pin_boton.value() == 1:
        desactivar_PAE("tocoboton") #pudo tocar el boton de reaccion

while True:
    exchange_data(station1, station2)
