try:
    import usocket as socket
except:
    import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import time, json, _thread
from machine import Timer
import machine

def conectar_wifi():
    global s
    print("holawifi")
    #configuracion
    addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]
    ssid = 'ESP32'
    password = 'aeroalert'

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
    s.listen(2)
    print("listening on",addr)
    
    return s


def escuchar_tipos():
    time.sleep(1)
    global s, ap, addr
    print("escuchar tipos xd")
    while True:
        
        print("1")
        conn, addr = s.accept()
        print('Got a type connection from %s' % str(addr))
        message = conn.recv(1024)
        
        tipo = json.loads(message.decode('utf-8'))
        
        if tipo == "soy_band":
            _thread.start_new_thread(escuchar_band, (conn, addr))
           
            
        
        elif tipo == "soy_rtdc":
            escuchar_rtdc(conn, addr)
            _thread.start_new_thread(escuchar_rtdc, (conn, addr))
            _thread.start_new_thread(enviar_rtdc, (conn, addr))

def escuchar_rtdc(conn_rtdc,addr):
    while True:
        message = conn_rtdc.recv(1024)
        print('Got a connection from rtdc %s' % str(addr))
        data = json.loads(message.decode('utf-8'))
        #recibe los comandos de vuelo enviados por la rtdc    


def escuchar_band(conn_band, addr):
    time.sleep(1)
    while True:
        message = conn_band.recv(1024)
        print()
        print('Got a connection from band %s' % str(addr))
    
        data = json.loads(message.decode('utf-8'))  #.decode('utf-8')
        bpm = data['1']
        spo = data['2']
        temp = data['3']
        conectado = data['4']
        print(data)
        print("bpm={:02} spo= {:02}% Temp {:02}°C ...conectado= {:1}".format(bpm, spo, temp, conectado))
        evaluar_info(bpm, spo, temp, conectado)
        
        

            
listabpm = []
listaspo = []
bpm_bajos1 = bpm_altos1 = spo_bajos1 = dormido1 = temp_baja1 = temp_alta1 = 0 

def pines_prueba():
    bpm_bajos2 = 0 #pin
    bpm_bajos2 = 0# pin
    bpm_altos2 = 0# pin
    spo_bajos2= 0# pin
    dormido2 =   0# pin
    temp_baja2 = 0# pin
    temp_alta2 = 0# pin


bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1 = 0,0,0,0,0,0
bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2 = 0,0,0,0,0,0
tomar_control = 0

codigo = [
                  bpm_altos1, bpm_altos2, 
                  bpm_bajos1, bpm_bajos2, 
                  dormido1, dormido2,
                  spo_bajos1, spo_bajos2, 
                  temp_alta1, temp_alta2, 
                  temp_baja1, temp_baja2,
                  tomar_control
                  ]
def actualizar_codigo():
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1
    global bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2
    global tomar_control
    global codigo
    codigo = [
              bpm_altos1, bpm_altos2, 
              bpm_bajos1, bpm_bajos2, 
              dormido1, dormido2,
              spo_bajos1, spo_bajos2, 
              temp_alta1, temp_alta2, 
              temp_baja1, temp_baja2,
              tomar_control
              ]
    return codigo

def enviar_rtdc(conn, addr):

    global codigo
    while True:
        print("enviando a RTDC: ", addr)
        
        codigo = actualizar_codigo()

        
        codigo_enviar = json.dumps(codigo).encode('utf-8')
        print(codigo)
        conn.send(codigo_enviar)
        time.sleep(10)
        


# Configurar los pines de la luz y el botón
pin_luz_amarilla = machine.Pin(5, machine.Pin.OUT)
pin_reaccion = machine.Pin(4, machine.Pin.IN)

pin_boton_reaccion = pin_reaccion.value()

pin_luz_alarma = machine.Pin(12, machine.Pin.OUT) #6

pin_luz_dormido = machine.Pin(14, machine.Pin.OUT) # 7

pin_luz_roja = machine.Pin(27, machine.Pin.OUT) #8


#para contador
pasaron_30segs_spo = pasaron_30segs_bpm_b = pasaron_30segs_bpm = 0
contador_iniciado_60_bpm = contador_iniciado_60_spo = contador_iniciado_60_bpm_b = 0
contador_iniciado_30_bpm = contador_iniciado_30_spo = contador_iniciado_30_bpm_b = 0
tomar_control = alarmas_off_spo = alarmas_off_bpm = alarmas_off_bpm_b = 0
            
t30spo = Timer(0)
t60spo = Timer(0)
t30bpm = Timer(0)
t60bpm = Timer(0)
t30bpm_b = Timer(0)
t60bpm_b = Timer(0)

def contador(cual):
    global alarmas_off_bpm, alarmas_off_bpm_b
    global alarmas_off_spo


    if cual == "60spo":
        global contador_iniciado_60_spo
        contador_iniciado_60_spo = 0
        alarmas_off_spo = 0
    elif cual == "30spo":
        global pasaron_30segs_spo
        pasaron_30segs_spo = 1
        alarmas_off_spo = 0



    elif cual == "30bpm":
        global pasaron_30segs_bpm
        pasaron_30segs_bpm = 1
        alarmas_off_bpm = 0
    elif cual == "60bpm":
        global contador_iniciado_60_bpm
        contador_iniciado_60_bpm = 1
        alarmas_off_bpm = 0


    elif cual == "30bpm_b":
        global pasaron_30segs_bpm_b
        pasaron_30segs_bpm_b = 1
        alarmas_off_bpm_b = 0
    elif cual == "60bpm_b":
        global contador_iniciado_60_bpm_b
        contador_iniciado_60_bpm_b = 0
        alarmas_off_bpm_b = 0



def activar_SAE():
    time.sleep(1)
    global codigo
    global pasaron_30segs_spo, pasaron_30segs_bpm_b, pasaron_30segs_bpm
    global contador_iniciado_60_bpm, contador_iniciado_60_spo, contador_iniciado_60_bpm_b
    global contador_iniciado_30_bpm, contador_iniciado_30_spo, contador_iniciado_30_bpm_b
    global tomar_control, alarmas_off_spo, alarmas_off_bpm, alarmas_off_bpm_b
    tocado = pin_reaccion.value()
    pin_boton_reaccion = 0
    #------------------------------------------
    while True:
        time.sleep(3)
        codigo = actualizar_codigo()
        print(codigo)
        print()
        

                    #si el boton de reaccion cambio de valor no va a valer lo que valia antes
        if pin_reaccion.value() != tocado:
            tocado = pin_reaccion.value()   #guarda el valor actual del pin
            pin_boton_reaccion = 1          #pone en 1 la variable que se va a usar para saber si se presiono
            

        #protocolo hipoxia
        if codigo[6]==1 and codigo[7]==1:               #si ambos tienen 6 y 7 activos (hipoxia)
               
            if alarmas_off_spo == 0:                    #si las alarmas no estan desactivadas
                pin_luz_alarma.value(1)                 #activa luz alarma (hipoxia?
                #alarma sonora tmb deberia


                if pin_boton_reaccion == 1:             #si el boton de reaccion fue presionado
                    alarmas_off_spo = 1                 #las alarmas de spo2 se desactivan
                    tomar_control = 0                   #se pone en 0 el pin de tomar el control
                    if contador_iniciado_60_spo != 1:   #si el contador de 60s spo2 no esta iniciado
                        t60spo.init(mode=Timer.ONE_SHOT, period=60000, callback=contador, args="60spo") #lo inicia
                        contador_iniciado_60_spo = 1    #cambia la variable para que la prox sepa que esta activado


                elif contador_iniciado_30_spo != 1:     #sino si el contador de 30s spo2 no esta iniciado
                    t30spo.init(mode=Timer.ONE_SHOT, period=30000, callback=contador, args="30spo")
                    contador_iniciado_30_spo = 1        #pone la variable en 1  cont_init_30spo

                elif pasaron_30segs_spo == 1:           #sino si pasaron30segsspo2 esta en 1
                    contador_iniciado_30_spo = 0        #pone en 0 la variable de cont_init_30spo
                    if pin_boton_reaccion != 1:         #si el pin de reaccion no es 1
                        tomar_control = 1               #pone pin tomar control en 1


            elif alarmas_off_spo == 1:                  #sino si estan desactivadas las alarmas spo
                pin_luz_alarma.value(0)                 #apaga luz alarma
                pass

        elif codigo[6]==1 or codigo[7]==1:              #sino si 1 tiene spo2 en 1
            print("1 piloto tiene hipoxia")
            pin_luz_roja.value(1)
        elif codigo[6]==0 and codigo[7]==0:             #sino si ninguno tiene spo2 en 1
            print("ningun piloto tiene hipoxia")
            pin_luz_amarilla.value(0)

        #------------------------------------------
        
        
        #protocolo pulsaciones altas
        if codigo[0]==1 and codigo[1]==1:        
            if alarmas_off_bpm == 0:
                pin_luz_alarma.value(1)
                #alarma sonora tmb


                if pin_boton_reaccion == 1:
                    alarmas_off_bpm = 1
                    tomar_control = 0
                    if contador_iniciado_60_bpm != 1:
                        t60bpm.init(mode=Timer.ONE_SHOT, period=6000, callback=contador, args="60bpm")
                        contador_iniciado_60_bpm = 1


                elif contador_iniciado_30_bpm != 1:
                    contador_iniciado_30_bpm = 1
                    t30bpm.init(mode=Timer.ONE_SHOT, period=3000, callback=contador, args="30bpm")
                
                elif pasaron_30segs_bpm == 1:
                    contador_iniciado_30_bpm = 0
                    if pin_boton_reaccion != 0:
                        tomar_control = 1


            elif alarmas_off_bpm == 1:
                pin_luz_alarma.value(0)
                pass


        elif codigo[0]==1 or codigo[1]==1:
            print("pulsaciones altas 1 piloto")
            pin_luz_amarilla.value(1)
        elif codigo[0]==0 and codigo[1]==0: #pulsaciones altas
            print("ninguno de los 2 pilotos tine pulsaciones altas")
            pin_luz_amarilla.value(0)

        #------------------------------------------
        
        
        #protocolo pulsaciones bajas
        if codigo[2]==1 and codigo[3]==1:                   #si ambos tienen    
            if alarmas_off_bpm_b != 1:                      #si las alarmas no estan desactivadas
                pin_luz_alarma.value(1)                     #PRENDE luz de alarma
                #alarma sonora tmb

                if pin_boton_reaccion == 1:                 #si el boton esta presionado
                    alarmas_off_bpm_b = 1                   #DESACTIVA las alarmas
                    tomar_control = 0                       #no permite que tomen el control
                    if contador_iniciado_60_bpm_b != 1:     #si no esta iniciado el contador 60s
                        t60bpm_b.init(mode=Timer.ONE_SHOT, period=6000, callback=contador, args="60bpm_b")
                                                            #INICIA temporizador, luego apagara la variable del contador 60s
                        contador_iniciado_60_bpm_b = 1      #PRENDE variable del contador 60s

                elif contador_iniciado_30_bpm_b != 1:       #sino, si no esta iniciado contador de 30s          
                    t30bpm_b.init(mode=Timer.ONE_SHOT, period=3000, callback=contador, args="30bpm_b")
                                                            #INICIAtemporizador, luego apagara la variable del contador 30s
                    contador_iniciado_30_bpm_b = 1          #PRENDE variable del contador 30s

                elif pasaron_30segs_bpm_b == 1:             #sino, si pasaron 30s
                    contador_iniciado_30_bpm_b = 0          #APAGA variable del contador iniciado 30s, porque ya paso
                    if pin_boton_reaccion != 1:             #si el boton de reaccion no esta presionado
                        tomar_control = 1                   #deja que tomen el control

            elif alarmas_off_bpm_b == 1:                    #sino, si estan apagadas las alarmas
                pin_luz_alarma.value(0)                     #apaga luz alarma
                pass

        elif codigo[2]==1 or codigo[3]==1:                  #sino son ambos, si alguno tiene
            print("pulsaciones bajas 1 piloto")
            pin_luz_amarilla.value(1)                       #prende luz
        elif codigo[2]==0 and codigo[3]==0:                 #si ninguno tiene
            print("ninguno de los 2 pilotos tine pulsaciones bajas")
            pin_luz_amarilla.value(0)                       #prende luz
        
        
        #------------------------------------------

        if dormido1 == 1:
            pin_luz_dormido.value(1)
            print("el piloto esta dormido")
        else:
            pin_luz_dormido.value(0)
            print("el piloto esta despierto")

        if pin_boton_reaccion == 1:
            pin_boton_reaccion = 0



def evaluar_info(bpm, spo, temp, conectado):
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1
    global listabpm, listaspo


    #Listas de pulsaciones y oxigeno
    listabpm.append(bpm)
    listabpm = listabpm[-48:]
    listaspo.append(spo)
    listaspo = listaspo[-48:] #12 valores cada uno cada 5 segs son 60 segs en total
    
    #dormido
    
     
    #suma de primeros 7 digitos de la lista
    bpm_prom_inicial = sum(listabpm[0:7])
    #suma de los ultimos 8 digitos de la lista
    bpm_prom_actual = sum(listabpm[:-8:-1])
    #diferencia entre ambos
    bpm_dif = bpm_prom_actual - bpm_prom_inicial
    

    spo_prom_inicial = sum(listabpm[0:7])
    spo_prom_actual = sum(listabpm[:-8:-1])
    spo_dif = spo_prom_actual - spo_prom_inicial


    if spo_dif >= 3 and spo_dif <= 8:
        if bpm_dif >= 15 and bpm_dif <= 35:
            print("tiene menos pulsaciones y oxigeno que hace un ratito, suponemos que esta dormido")
            dormido1 = 1
            bpm_dormido = bpm
            spo_dormido = spo


    if dormido1 == 1:
        bpm_dormido_dif = bpm - bpm_dormido
        spo_dormido_dif = spo - spo_dormido
        if bpm_dormido_dif >= 20:
            if spo_dormido_dif >= 3:
                print("esta despierto ahora")
                dormido1 = 0
    #despierto

    #bpms
    if bpm < 60:
        bpm_bajos1 = 1
        bpm_altos1 = 0
    elif bpm > 140:
        bpm_altos1 = 1
        bpm_bajos1 = 0
    else:
        bpm_bajos1 = 0
        bpm_altos1 = 0
    
    #spo
    if spo <= 90:
        spo_bajos1 = 1
    elif spo > 90:
        spo_bajos1 = 0
    
    #segun temperaturas:
    if temp < 5:
        temp_baja1 = 1
        temp_alta1 = 0
    elif temp > 40:
        temp_alta1 = 1
        temp_baja1 = 0
    else:
        temp_baja1 = 0
        temp_alta1 = 0  


s = conectar_wifi()
print("hola13")

_thread.start_new_thread(activar_SAE, ())
print("2thread")
time.sleep(1)
_thread.start_new_thread(escuchar_tipos, ())
print("1thread")


#_thread.start_new_thread(recibir_band2, (station3,))
#exchange_data2(station2)
#exchange_data1(station1)
