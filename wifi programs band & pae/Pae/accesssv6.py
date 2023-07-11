try:
    import usocket as socket
except:
    import socket
import network
import esp, gc
esp.osdebug(None)
gc.collect()
import random, json, time
from machine import Timer
import machine
from wifi_connection import connect_wifi

s = connect_wifi()

listabpm = []
listaspo2 = []
bpm_bajos1 = bpm_altos1 = spo2_bajos1 = dormido1 = temp_baja1 = temp_alta1 = 0 
bpm_bajos2 = 0# pin
bpm_altos2 = 0# pin
spo2_bajos2= 0# pin
dormido2 =   0# pin
temp_baja2 = 0# pin
temp_alta2 = 0# pin
tomar_control = 0

station1, addr1 = s.accept()
print('Conexión establecida con el ESP32 como estación 1(rtdc):', addr1)

#station2, addr2 = s.accept()
#print('Conexión establecida con el ESP32 como estación 2(band):', addr2)

station3 = 3 # la pulsera del copiloto

def recibir_band1(estacion2):
    while True:
        message2 = estacion2.recv(1024)
        print(message2.decode('utf-8'))
        evaluar_info(message2)
        

def recibir_rtdc(estacion1):
    while True: 
        message1 = estacion1.recv(1024)
        print('Datos recibidos:', message1.decode('utf-8'))
        
def enviar_rtdc(rtdc):
    global bpm_bajos1, bpm_altos1, spo2_bajos1, dormido1, temp_baja1, temp_alta1
    global bpm_bajos2, bpm_altos2, spo2_bajos2, dormido2, temp_baja2, temp_alta2
    global tomar_control
    global codigo
    while True:
        codigo = [bpm_altos1,bpm_altos2, bpm_bajos1,bpm_bajos2, dormido1,dormido2,
                   spo2_bajos1,spo2_bajos2, tomar_control]
        codigo_enviar = json.dumps(codigo).encode('utf-8')
        print(codigo)
        #rtdc.send(codigo_enviar)
        time.sleep(10)

# Configurar los pines de la luz y el botón
pin_luz_amarilla = machine.Pin(5, machine.Pin.OUT)
pin_boton_reaccion = machine.Pin(4, machine.Pin.IN)
pin_luz_alarma = machine.Pin(6, machine.Pin.OUT)
pin_luz_dormido = machine.Pin(7, machine.Pin.OUT)

pasaron_30segs_spo2 = pasaron_30segs_bpm_b = pasaron_30segs_bpm = 0
contador_iniciado_60_bpm = contador_iniciado_60_spo2 = contador_iniciado_60_bpm_b = 0
contador_iniciado_30_bpm = contador_iniciado_30_spo2 = contador_iniciado_30_bpm_b = 0
tomar_control = alarmas_off_spo2 = alarmas_off_bpm = alarmas_off_bpm_b = 0
            
t30spo2 = Timer(0)
t60spo2 = Timer(0)
t30bpm = Timer(0)
t60bpm = Timer(0)
t30bpm_b = Timer(0)
t60bpm_b = Timer(0)

def contador(cual):
    if cual == "30spo2":
        global pasaron_30segs_spo2, alarmas_off_spo2
        pasaron_30segs_spo2 = 1
        alarmas_off_spo2 = 0
    elif cual == "60spo2":
        global contador_iniciado_60_spo2, alarmas_off_spo2
        contador_iniciado_60_spo2 = 0
        alarmas_off_spo2 = 0

    elif cual == "30bpm":
        global pasaron_30segs_bpm, alarmas_off_bpm
        pasaron_30segs_bpm = 1
        alarmas_off_bpm = 0
    elif cual == "60bpm":
        global contador_iniciado_60_bpm, alarmas_off_bpm
        contador_iniciado_60_bpm = 1
        alarmas_off_bpm = 0

    elif cual == "30bpm_b":
        global pasaron_30segs_bpm_b, alarmas_off_bpm_b
        pasaron_30segs_bpm_b = 1
        alarmas_off_bpm_b = 0
    elif cual == "60bpm_b":
        global contador_iniciado_60_bpm_b, alarmas_off_bpm_b
        contador_iniciado_60_bpm_b = 1
        alarmas_off_bpm_b = 0

def activar_SAE():
    global codigo
    global pasaron_30segs_spo2, pasaron_30segs_bpm_b, pasaron_30segs_bpm
    global contador_iniciado_60_bpm, contador_iniciado_60_spo2, contador_iniciado_60_bpm_b
    global contador_iniciado_30_bpm, contador_iniciado_30_spo2, contador_iniciado_30_bpm_b
    global tomar_control, alarmas_off_spo2, alarmas_off_bpm, alarmas_off_bpm_b
    
    #------------------------------------------
    #protocolo hipoxia
    if codigo[6]==1 or codigo[7]==1:
        print("1 piloto tiene hipoxia")
        pin_luz_amarilla.value(1)
    elif codigo[6]==0 and codigo[7]==0:
        print("ningun piloto tiene hipoxia")
        pin_luz_amarilla.value(0)

    if codigo[6]==1 and codigo[7]==1:        
        if alarmas_off_spo2 == 0:
            pin_luz_alarma.value(1)
            #alarma sonora tmb
            if pin_boton_reaccion == 1:
                alarmas_off_spo2 = 1
                tomar_control = 0
                if contador_iniciado_60_spo2 == 0:
                    t60spo2.init(mode=Timer.ONE_SHOT, period=6000, callback=contador, args="60spo2")
                    contador_iniciado_60_spo2 = 1

            elif contador_iniciado_30_spo2 == 0:
                contador_iniciado_30_spo2 = 1
                t30spo2.init(mode=Timer.ONE_SHOT, period=3000, callback=contador, args="30spo2")
            
            elif pasaron_30segs_spo2 == 1:
                contador_iniciado_30_spo2 = 0
                if pin_boton_reaccion == 0:
                    tomar_control = 1
        elif alarmas_off_spo2 == 1:
            pin_luz_alarma.value(0)
            pass
    #------------------------------------------
    #protocolo pulsaciones altas
    if codigo[0]==1 or codigo[1]==1:
        print("pulsaciones altas 1 piloto")
        pin_luz_amarilla.value(1)
    elif codigo[0]==0 and codigo[1]==0: #pulsaciones altas
        print("ninguno de los 2 pilotos tine pulsaciones altas")
        pin_luz_amarilla.value(0)

    if codigo[0]==1 and codigo[1]==1:        
        if alarmas_off_bpm == 0:
            pin_luz_alarma.value(1)
            #alarma sonora tmb
            if pin_boton_reaccion == 1:
                alarmas_off_bpm = 1
                tomar_control = 0
                if contador_iniciado_60_bpm == 0:
                    t60bpm.init(mode=Timer.ONE_SHOT, period=6000, callback=contador, args="60bpm")
                    contador_iniciado_60_bpm = 1

            elif contador_iniciado_30_bpm == 0:
                contador_iniciado_30_bpm = 1
                t30bpm.init(mode=Timer.ONE_SHOT, period=3000, callback=contador, args="30bpm")
            
            elif pasaron_30segs_bpm == 1:
                contador_iniciado_30_bpm = 0
                if pin_boton_reaccion == 0:
                    tomar_control = 1
        elif alarmas_off_bpm == 1:
            pin_luz_alarma.value(0)
            pass
    

    #------------------------------------------
    #protocolo pulsaciones bajas
    if codigo[2]==1 or codigo[3]==1:
        print("pulsaciones bajas 1 piloto")
        pin_luz_amarilla.value(1)
    elif codigo[2]==0 and codigo[3]==0: #pulsaciones altas
        print("ninguno de los 2 pilotos tine pulsaciones bajas")
        pin_luz_amarilla.value(0)

    if codigo[2]==1 and codigo[3]==1:        
        if alarmas_off_bpm_b == 0:
            pin_luz_alarma.value(1)
            #alarma sonora tmb
            if pin_boton_reaccion == 1:
                alarmas_off_bpm_b = 1
                tomar_control = 0
                if contador_iniciado_60_bpm_b == 0:
                    t60bpm_b.init(mode=Timer.ONE_SHOT, period=6000, callback=contador, args="60bpm_b")
                    contador_iniciado_60_bpm_b = 1

            elif contador_iniciado_30_bpm_b == 0:
                contador_iniciado_30_bpm_b = 1
                t30bpm_b.init(mode=Timer.ONE_SHOT, period=3000, callback=contador, args="30bpm_b")
            
            elif pasaron_30segs_bpm_b == 1:
                contador_iniciado_30_bpm_b = 0
                if pin_boton_reaccion == 0:
                    tomar_control = 1
        elif alarmas_off_bpm_b == 1:
            pin_luz_alarma.value(0)
            pass
    #------------------------------------------

    if dormido1 == 1:
        pin_luz_dormido.value(1)
        print("el piloto esta dormido")
    else:
        pin_luz_dormido.value(0)
        print("el piloto esta despierto")
    
def evaluar_info(message):
    global bpm_bajos1, bpm_altos1, spo2_bajos1, dormido1, temp_baja1, temp_alta1

    data1 = json.loads(message.decode('utf-8'))
    bpm = data1['value1']
    spo2 = data1['value2']
    temp = data1['value3']
    print("bpm={:02} SpO2= {:02}% Temp {:02}°C".format(bpm, spo2, temp))  #borrar
    
    listabpm.append(bpm)
    listabpm = listabpm[-48:]
    listaspo2.append(spo2)
    listaspo2 = listaspo2[-48:] #12 valores cada uno cada 5 segs son 60 segs en total
    
    #dormido
    bpm_inicial = listabpm[1,2,3,4,5,6]
    bpm_prom = sum(bpm_inicial)
    bpm_dif = bpm_prom - bpm_inicial
    spo2_inicial = listaspo2[1,2,3,4,5,6]
    spo2_prom = sum(spo2_inicial)
    spo2_dif = spo2_prom - spo2_inicial

    if spo2_dif >= 3 and spo2_dif <= 8:
        if bpm_dif >= 15 and bpm_dif <= 35:
            print("tiene menos pulsaciones y menos oxigeno que hace un ratito entonces puede estar dormido")
            dormido1 = 1
            bpm_dormido = bpm
            spo2_dormido = spo2
    bpm_dormido_dif = bpm - bpm_dormido
    spo2_dormido_dif = spo2 - spo2_dormido

    if bpm_dormido_dif >= 20:
        if spo2_dormido_dif >= 3:
            print("esta despierto ahora")
            dormido = 0
    #despierto

    #bpms
    if bpm < 50:
        bpm_bajos1 = 1
    elif bpm > 140:
        bpm_altos1 = 1
    else:
        bpm_bajos1 = 0
        bpm_altos1 = 0
    
    #spo2
    if spo2 <= 90:
        spo2_bajos1 = 1
    elif spo2 > 90:
        spo2_bajos1 = 0
    
    #segun temperaturas:
    if temp < 5:
        temp_baja1 = 1
    elif temp > 40:
        temp_alta1 = 1
    else:
        temp_baja1 = 0
        temp_alta1 = 0  

#_thread.start_new_thread(recibir_rtdc, (station1,))
#_thread.start_new_thread(enviar_rtdc, (station1,))
_thread.start_new_thread(recibir_band1, (station2,))
#_thread.start_new_thread(recibir_band2, (station3,))
#exchange_data2(station2)
#exchange_data1(station1)