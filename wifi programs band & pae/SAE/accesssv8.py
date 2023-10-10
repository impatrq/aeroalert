try:
    import usocket as socket
except:
    import socket
import esp
esp.osdebug(None)
import gc
gc.collect()
import time, json, _thread
import machine, network
from machine import Timer, UART




def definir_pines():

    global pin_luz_ambar, pin_luz_roja, pin_luz_test, pin_flag
    global pin_activacion_manual, pin_test, pin_reaccion, pin_on_off
    global pin_boton_test, pin_boton_reaccion, pin_boton_on_off

    #21
    #19
    pin_luz_ambar = machine.Pin(23, machine.Pin.IN)             
    pin_luz_roja = machine.Pin(5, machine.Pin.IN)              
    pin_luz_test = machine.Pin(17, machine.Pin.IN)                      
    
    pin_activacion_manual = machine.Pin(4, machine.Pin.IN)
    pin_activacion_manual.value()

    pin_test = machine.Pin(25, machine.Pin.IN)                   
    pin_boton_test = pin_test.value()
    
    pin_reaccion = machine.Pin(33, machine.Pin.IN)
    pin_boton_reaccion = pin_reaccion.value()                
    
    pin_on_off = machine.Pin(35, machine.Pin.IN)      

    pin_flag = machine.Pin(25, machine.Pin.OUT)      #Correcto    

definir_pines()


def conectar_wifi():
    global s, ap
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
    print("Escuchando tipos")
    while True:
        conn, addr = s.accept()
        print('Got a type connection from %s' % str(addr))
        message = conn.recv(1024)
        tipo = json.loads(message.decode('utf-8'))
        
        if tipo == "soy_band":
            _thread.start_new_thread(escuchar_band, (conn, addr))
        
        elif tipo == "soy_rtdc":
            _thread.start_new_thread(escuchar_rtdc, (conn, addr))
            _thread.start_new_thread(enviar_rtdc, (conn, addr))
        
        elif tipo == "soy_PC":
            _thread.start_new_thread(escuchar_PC, (conn, addr))
            _thread.start_new_thread(enviar_PC, (conn, addr))



def escuchar_band(conn_band, addr):
    time.sleep(1)
    while True:
        message = conn_band.recv(1024)
        print()
        print('From Band %s' % str(addr))
    
        data = json.loads(message.decode('utf-8'))  #.decode('utf-8')
        bpm = data['1']
        spo = data['2']
        temp = data['3']
        conectado = data['4']
        print("bpm={:02} spo={:02}% Temp={:02}°C puesta={:1}".format(bpm, spo, temp, conectado))
        evaluar_info(bpm, spo, temp, conectado, "band")    

aterrizar = aterrizar_manual = 0
def escuchar_rtdc(conn_rtdc,addr):
    global aterrizar
    pin_flag.value(0)
    try:
        while True:
            data = conn_rtdc.recv(1024)
            print('From RTDC %s' % str(addr))

            message = json.loads(data.decode('utf-8'))
            print(message)

            if message['mensage'] == "aterriza":
                print("tiene que aterrizar")                        #ATERRIZAR ATERRIZAR ATERRIZAR ATERRIZAR 
                aterrizar = 1                                                
            if message['mensage'] == "no aterrizar":
                aterrizar = 0
    except:
        pin_flag.value(1)
        # Recibe los comandos de vuelo enviados por la rtdc 
        # HAY QUE EVALUAR ESTA INFORMACION Y MANDAR LO CORRESPONDIENTE AL XPLANE   


        #recibir rtdc intentional loss se prende luz roja parpadeando

def enviar_rtdc(conn, addr):
    global codigo, solicitar, info_aeropuerto
    alerta_enviada = 0
    solicito_aterrizaje = json.dumps("solicito aterrizaje").encode('utf-8')
    alerta_desactivacion_sae = json.dumps("alerta desactivacion del sae").encode('utf-8')
    sae_activado = json.dumps("Sae activado").encode('utf-8')
    try:
        while True:
            print("enviando a RTDC: ", addr)
            
            if solicitar == 1:
                conn.send(solicito_aterrizaje)
                solicitar = 0
                info_aeropuerto = conn.recv(1024)

            codigo = actualizar_codigo()
            codigo_enviar = json.dumps(codigo).encode('utf-8')
            conn.send(codigo_enviar)
            if pin_on_off.value() == 1 and alerta_enviada == 0:
                codigo_enviar = alerta_desactivacion_sae
                conn.send(codigo_enviar)
                alerta_enviada = 1
            elif pin_on_off.value() == 0 and alerta_enviada == 1:
                codigo_enviar = sae_activado
                conn.send(codigo_enviar)
                alerta_enviada = 0
            time.sleep(10)
    except:
        print("rtdc perdida")


def escuchar_PC(conn_PC, addr):
    global bloqueo_PC
    global dormido1, spo_bajos1, bpm_altos1, muerte1
    #pin_on_off.value(0)
    estados = {"Piloto1":{"Somnolencia":0, "Pulso":0, "Hipoxia": 0, "Muerte": 0, "Spo2": 0, "Bpm":0},
               "Piloto2":{"Somnolencia":0, "Pulso":0, "Hipoxia": 0, "Muerte": 0, "Spo2": 0, "Bpm":0}
               }
    bloqueo_PC = 0

    while True:
        time.sleep(3)         
        if pin_on_off.value() == 1:
            pass
        else:
            message = conn_PC.recv(1024)
            print()
            print('Got a connection from PC %s' % str(addr))            # info_PC = {"Piloto":1, 
            info_PC = json.loads(message.decode('utf-8'))               # "Somnolencia": 1, "Pulso":1, 
            print("PC recibido")                                        # "Spo2":92, "Hipoxia":1,
            print(info_PC)

            if info_PC == "1":
                
                if bloqueo_PC == 0:
                    bloqueo_PC = 1 
                elif bloqueo_PC == 1:
                    bloqueo_PC = 0
                                    
                if int(estados["Piloto1"]["Bpm"]) != 0 and int(estados["Spo2"]) != 0:
                    bloqueo_PC = 1                                      
                    evaluar_info(estados["Piloto1"]["Bpm"], estados["Piloto1"]["Spo2"], 15, 1, "PC")
                else:
                
                    if estados["Piloto1"]["Pulso"] == '1':
                        bpm_altos1 = 1            
                    else:
                        bpm_altos1 = 0

                    if estados["Piloto1"]["Hipoxia"] == '1':
                        spo_bajos1 = 1            
                    else:
                        spo_bajos1 = 0

                    if estados["Piloto1"]["Muerte"] == '1':
                        muerte1 = 1
                    else:
                        muerte1 = 0
                if estados["Piloto1"]["Somnolencia"] == '1':
                    dormido1 = 1            
                else:
                    dormido1 = 0
            
                evaluar_info_piloto2(estados["Piloto2"])
                
            elif info_PC["Piloto"] == '1':
                info_PC.pop("Piloto")
                estados["Piloto1"] = info_PC
            elif info_PC["Piloto"] == '2':
                info_PC.pop("Piloto")
                estados["Piloto2"] = info_PC

            print(estados)
            
            
def enviar_PC(conn, addr):
    global aterrizar, aterrizar_manual, solicitar, info_aeropuerto
    enviado = 0
    aterrizar = json.dumps("ATERRIZAR").encode('utf-8')
    no_aterrizar = json.dumps("NO ATERRIZAR").encode('utf-8')
    while True:
        # pedir permiso para aterrizar antes a rtdc


        if aterrizar == 1 and enviado == 0 or aterrizar_manual == 1 and enviado == 0:
            solicitar = 1
            print("aterrizar a PC: ", addr)
            conn.send(aterrizar)
            enviado = 1
            
            while True:
                if info_aeropuerto != 0:
                    conn.send(json.dumps(info_aeropuerto).encode('utf-8'))
                    info_aeropuerto = 0
                    break

        elif aterrizar_manual == 0 and aterrizar == 0 and enviado == 1:
            print("no aterrizar a PC: ", addr)
            conn.send(no_aterrizar)
            enviado = 0

        time.sleep(5)


def evaluar_info_piloto2(info):
    global bpm_altos2, spo_bajos2, dormido2, muerte2
    if info["Pulso"] == '1':
        bpm_altos2 = 1
    else:
        bpm_altos2 = 0
    
    if info["Hipoxia"] == '1':
        spo_bajos2 = 1
    else:
        spo_bajos2 = 0

    if info["Somnolencia"] == '1':
        dormido2 = 1
    else:
        dormido2 = 0
    if info["Muerte"] == '1':
        muerte2 = 1
    else:
        muerte2 = 0

    return



bpm_bajos1 = bpm_altos1 = spo_bajos1 = dormido1 = temp_baja1 = temp_alta1 = 0 
bpm_bajos2 = bpm_altos2 = spo_bajos2 = dormido2 = temp_baja2 = temp_alta2 = 0
muerte1 = muerte2 = 0
manual = pulsera_conectada = 0
codigo = [
        bpm_altos1, bpm_altos2, 
        bpm_bajos1, bpm_bajos2, 
        dormido1, dormido2,
        spo_bajos1, spo_bajos2, 
        temp_alta1, temp_alta2, 
        temp_baja1, temp_baja2,
        muerte1, muerte2, 
        manual, pulsera_conectada
        ]


def actualizar_codigo():
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1
    global bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2 # se modifican directamente
    global muerte1, muerte2, manual, pulsera_conectada
    global codigo
    manual = pin_activacion_manual.value()
    codigo = [
              bpm_altos1, bpm_altos2, 
              bpm_bajos1, bpm_bajos2, 
              dormido1, dormido2,
              spo_bajos1, spo_bajos2, 
              temp_alta1, temp_alta2, 
              temp_baja1, temp_baja2,
              muerte1, muerte2, 
              manual, pulsera_conectada
              ]
    return codigo


#para contador
pasaron_30segs_spo = pasaron_30segs_bpm = 0
contador_iniciado_60_bpm = contador_iniciado_60_spo = 0
contador_iniciado_30_bpm = contador_iniciado_30_spo = 0
tomar_control = alarmas_off_spo = alarmas_off_bpm = 0
            
t30spo = Timer(0)
t60spo = Timer(0)
t30bpm = Timer(0)
t60bpm = Timer(0)


def contador60spo(self):
    global alarmas_off_bpm, alarmas_off_spo
    global contador_iniciado_60_spo
    contador_iniciado_60_spo = 0
    alarmas_off_spo = 0
def contador30spo(self):
    global alarmas_off_bpm, alarmas_off_spo
    global pasaron_30segs_spo
    pasaron_30segs_spo = 1
    alarmas_off_spo = 0
    
def contador30bpm(self):
    global alarmas_off_bpm, alarmas_off_spo
    global pasaron_30segs_bpm
    pasaron_30segs_bpm = 1
    alarmas_off_bpm = 0
    
def contador60bpm(self): 
    global alarmas_off_bpm, alarmas_off_spo
    global contador_iniciado_60_bpm
    contador_iniciado_60_bpm = 0
    alarmas_off_bpm = 0

def activar_SAE():
    time.sleep(1)
    global codigo, pulsera_conectada
    global pasaron_30segs_spo, pasaron_30segs_bpm
    global contador_iniciado_60_bpm, contador_iniciado_60_spo
    global contador_iniciado_30_bpm, contador_iniciado_30_spo
    global tomar_control, alarmas_off_spo, alarmas_off_bpm
    global aterrizar, aterrizar_manual
    tocado = pin_reaccion.value()
    pin_boton_reaccion = 0
    ambar_titilando = 0
    
    while True:
        time.sleep(1)
        if pin_on_off.value() == 1:
            pin_luz_ambar.value(0)
            pin_luz_roja.value(0)
            pass
        else:   
            # Luz roja titilar cuando activacion manual
            if pin_activacion_manual == 1:
                if prendido == 0:
                    aterrizar_manual = 1
                    pin_luz_roja.value(1)
                    prendido = 1
                elif prendido == 1:
                    pin_luz_roja.value(0)
                    prendido = 0
            else:
                aterrizar_manual = 0

            codigo = actualizar_codigo()
            print(codigo)
            print()  

            if ambar_titilando == 1:
                if pin_luz_ambar.value() == 0:
                    pin_luz_ambar.value(1)
                elif pulsera_conectada != 0:
                    pin_luz_ambar.value(0)
            elif ambar_titilando == 0:
                if pulsera_conectada != 0:
                    pin_luz_ambar.value(0)
            if pulsera_conectada == 0:
                pin_luz_ambar.value(1)


            # Boton tipo switch
            # Si el boton de reaccion cambio de valor no va a valer lo que valia antes
            if pin_reaccion.value() != tocado:
                tocado = pin_reaccion.value()                       # Guarda el valor actual del pin
                pin_boton_reaccion = 1               # Pone en 1 la variable que se va a usar para saber si se presiono
                

            #muerte 1 luz amarilla fija
            #2 muertos luz roja fija y sonido si por 30 segs no boton de reaccion  
            #avisa a rtdc emergencia 2 muertso




            # Protocolo hipoxia
            if codigo[6] and codigo[7]:                       # Si ambos tienen 6 y 7 activos (hipoxia)

                if alarmas_off_spo == 0:                            # Si las alarmas no estan desactivadas
                    pin_luz_roja.value(1)                           # Activa luz alarma (hipoxia?
# Alarma sonora tmb deberia     alarma = 1
                    
                    # Si el piloto toca el boton de reaccion desactiva las alarmas, no deja que tomen el control
                    # Tmb inicia un contador de 60segs que estara sin las alarmas
                    if pin_boton_reaccion == 1:                     # Si el boton de reaccion fue presionado
                        alarmas_off_spo = 1                         # Las alarmas de spo2 se desactivan
                        tomar_control = 0                           # Se pone en 0 el pin de tomar el control
                        if contador_iniciado_60_spo != 1:           # Si el contador de 60s spo2 no esta iniciado
                            t60spo.init(mode=Timer.ONE_SHOT, period=60000, callback=contador60spo) #Lo inicia
                            contador_iniciado_60_spo = 1            # Cambia la variable para que la prox sepa que esta activado


                    # Inicia contador 30 segs para definir hipoxia peligrosa
                    elif contador_iniciado_30_spo != 1:             # Sino si el contador de 30s spo2 no esta iniciado
                        t30spo.init(mode=Timer.ONE_SHOT, period=30000, callback=contador30spo)
                        contador_iniciado_30_spo = 1                # Pone la variable en 1  cont_init_30spo


                    # 30 segs despues de tener hipoxia y no tener reaccion deja que tomen el control
                    elif pasaron_30segs_spo == 1:                   # Sino si pasaron30segsspo2 esta en 1
                        contador_iniciado_30_spo = 0                # Pone en 0 la variable de cont_init_30spo
                        if pin_boton_reaccion != 1:                 # Si el pin de reaccion no es 1
                            tomar_control = 1                       # Pone pin tomar control en 1


                elif alarmas_off_spo == 1:                          # Sino si estan desactivadas las alarmas spo
                    pin_luz_roja.value(0)                           # Apaga luz alarma
                    pass        

            elif codigo[6] or codigo[7]:                            # Sino si 1 tiene spo2 en 1
                print("1 hipoxia")     
                pin_luz_roja.value(1)                             
# Apagar alarma sonora      alarma = 0
            elif not codigo[6] and not codigo[7]:                     # Sino si ninguno tiene spo2 en 1
                print("no hipoxia")
                pin_luz_roja.value(0)
  # Apagar alarma sonora      alarma = 0              


            #------------------------------------------
            

            #codigo 0 pulsaciones altas piloto 1
            #codigo 1 pulsaciones altas piloto 2
            #codigo 2 pulsaciones bajas piloto 1
            #codigo 3 pulsaciones bajas piloto 2
            
            #protocolo pulsaciones raras
            if codigo[0] and codigo[1] or codigo[2] and codigo[3] or codigo[0] and codigo[3] or codigo[1] and codigo[2]:   
                # Si ambos tienen    
                if alarmas_off_bpm != 1:                          # Si las alarmas no estan desactivadas
                    pin_luz_ambar.value(1)                          # DEBERIA TITILAR
                    ambar_titilando = 1

                    # Alarma sonora tmb

                    if pin_boton_reaccion == 1:                   # Si el boton esta presionado
                        alarmas_off_bpm = 1                       # DESACTIVA las alarmas
                        tomar_control = 0                           # No permite que tomen el control
                        if contador_iniciado_60_bpm != 1:         # Si no esta iniciado el contador 60s
                            t60bpm.init(mode=Timer.ONE_SHOT, period=6000, callback=contador60bpm)
                                            # INICIA temporizador, luego apagara la variable del contador 60s
                            contador_iniciado_60_bpm = 1          # PRENDE variable del contador 60s

                    elif contador_iniciado_30_bpm != 1:           # Sino, si no esta iniciado contador de 30s          
                        t30bpm.init(mode=Timer.ONE_SHOT, period=3000, callback=contador30bpm)
                                            # INICIAtemporizador, luego apagara la variable del contador 30s
                        contador_iniciado_30_bpm = 1              # PRENDE variable del contador 30s
        
                    elif pasaron_30segs_bpm == 1:                 # Sino, si pasaron 30s
                        contador_iniciado_30_bpm = 0              # APAGA variable del contador iniciado 30s, porque ya paso
                        if pin_boton_reaccion != 1:                 # Si el boton de reaccion no esta presionado
                            tomar_control = 1                       # Deja que tomen el control
        
                elif alarmas_off_bpm == 1:                        # Sino, si estan apagadas las alarmas
                    pin_luz_ambar.value(0)                          # DEBE DEJAR DE TITILAR
                    ambar_titilando = 0 
                    pass    
                    
            elif codigo[0] or codigo[1] or codigo[2] or codigo[3]:                      # Sino son ambos, si alguno tiene
                print("bpm 1") 
                pin_luz_ambar.value(1)                              # DEBERIA TITILAR
                ambar_titilando = 1 
            #alarma = 0
            elif not codigo[0] and not codigo[1] and not codigo[2] and not codigo[3]:   # Si ninguno tiene pulsaciones raras
                print("no bpm")
                if pulsera_conectada != 0:
                    pin_luz_ambar.value(0)                              # DEBE DEJAR DE TITILAR
                    ambar_titilando = 0
            #alarma = 0
            
            #------------------------------------------
            if ambar_titilando != 1:                                # Si no esta titilando
                if dormido1 == 1:   
                    pin_luz_ambar.value(1)                          # SIN TITILAR
                    print("dormido") 
                else:   
                    if pulsera_conectada != 0:
                        pin_luz_ambar.value(0)                          #SE APAGA
                        print("despierto")
            #-------------------------------------------------
            if pin_boton_reaccion == 1:
                pin_boton_reaccion = 0
            
            if codigo[12] and codigo[13]:
                print("ambos muertos")
                pin_luz_roja.value(1)
            elif codigo[12] or codigo[13]:
                print("uno muerto")
                pin_luz_roja.value(0)
                pin_luz_ambar.value(1)
            else:
                print("todos vivos")
                pin_luz_roja.value(0)
                pin_luz_roja.value(0)

                


listabpm = []
listaspo = []
def evaluar_info(bpm, spo, temp, conectado, de):
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1, muerte1
    global listabpm, listaspo           #se usa en distintos threads por eso global
    global bloqueo_PC
    global pulsera_conectada

    

    if bloqueo_PC == 0:          # se evalua la info si es de band sin bloqueo
        #Listas de pulsaciones y oxigeno
        #--------------------------------------------------------------------------
        pulsera_conectada = conectado
        listabpm.append(bpm)
        listabpm = listabpm[-48:]
        listaspo.append(spo)
        listaspo = listaspo[-48:] #12 valores cada uno cada 5 segs son 60 segs en total

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
        #--------------------------------------------------------------------------
        #bpms
    if bloqueo_PC == 0 or de == "PC":      
        if bpm < 60:
            bpm_bajos1 = 1
            bpm_altos1 = 0
        elif bpm > 140:
            bpm_altos1 = 1
            bpm_bajos1 = 0
        else:
            bpm_bajos1 = 0
            bpm_altos1 = 0

        if bpm == 0:
            muerte1 = 1
        elif bpm != 0:
            muerte1 = 0
        
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
print("wifi conectado")

_thread.start_new_thread(activar_SAE, ())
print("protocolos activados")
time.sleep(1)





_thread.start_new_thread(escuchar_tipos, ())
print("receptor activado")


#_thread.start_new_thread(recibir_band2, (station3,))
#exchange_data2(station2)
#exchange_data1(station1)
