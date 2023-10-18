import usocket as socket
import gc                                                                               #import esp
gc.collect()                                                                            #esp.osdebug(None)
import time, json, _thread
import network
from machine import Pin, Timer, UART


nro_vuelo = 7365458



def definir_pines():
    global pin_luz_ambar, pin_luz_roja, pin_luz_test, pin_flag
    global pin_activacion_manual, pin_test, pin_reaccion, pin_on_off
    global pin_boton_test, pin_boton_reaccion

    pin_luz_ambar = Pin(17, Pin.OUT)             
    pin_luz_roja = Pin(4, Pin.OUT)              
    pin_luz_test = Pin(14, Pin.OUT)        
    pin_flag = Pin(26, Pin.OUT)               
    pin_activacion_manual = Pin(21, Pin.IN)
    pin_on_off = Pin(35, Pin.IN)

    pin_test = Pin(18, Pin.IN)                   
    pin_boton_test = pin_test.value()
    
    pin_reaccion = Pin(19, Pin.IN)
    pin_boton_reaccion = pin_reaccion.value()

definir_pines()

def conectar_wifi():
    global s, ap
    # Configuracion
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
            print("VDB conectada")
        
        elif tipo == "soy_rtdc":
            _thread.start_new_thread(escuchar_rtdc, (conn, addr))
            _thread.start_new_thread(enviar_rtdc, (conn, addr))
            print("CTRT conectada")

        elif tipo == "soy_PC":
            _thread.start_new_thread(escuchar_PC, (conn, addr))
            _thread.start_new_thread(enviar_PC, ())
            print("PC/X-PLANE conectado")


def escuchar_band(conn_band, addr):
    time.sleep(1)
    while True:
        message = conn_band.recv(1024)
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
    global aterrizar, intentional_loss, info_aeropuerto
    pin_flag.value(0)
    try:
        while True:
            data = conn_rtdc.recv(1024)
            message = json.loads(data.decode('utf-8'))
            print('From RTDC %s' % str(addr))
            print(message)

            if message['mensaje'] == "aterriza":
                print("tiene que aterrizar")                        #ATERRIZAR ATERRIZAR ATERRIZAR ATERRIZAR 
                aterrizar = 1                                                
            elif message['mensaje'] == "no aterrizes":
                print("no tiene que aterrizar")
                aterrizar = 0

            elif message['mensaje'] == type(dict):
                info_aeropuerto = message['mensaje']['info aeropuerto']

            elif message['mensaje'] == "intentional loss":
                intentional_loss = 1
                print("prender alarma Aes activation")
            elif message['mensaje'] == "apagar intentional loss":
                intentional_loss = 0
                print("apagar alarma Aes activation")
    except:
        pin_flag.value(1)
        # Recibe los comandos de vuelo enviados por la rtdc 

    #recibir rtdc intentional loss se prende luz roja parpadeando

def enviar_rtdc(conn, addr):
    global solicitar, info_aeropuerto, nro_vuelo
    alerta_enviada = 0
    try:
        while True:
            print("enviando a RTDC: ", addr)
            msg = ""

            if pin_on_off.value() == 1 and alerta_enviada == 0:
                msg = "alerta_desactivacion_sae"
                alerta_enviada = 1
            elif pin_on_off.value() == 0 and alerta_enviada == 1:
                msg = "sae_activado"                
                alerta_enviada = 0
 
            codigo = actualizar_codigo()
            dicc = {"msg":msg, "list":codigo, "nro_vuelo":nro_vuelo}
            codigo_enviar = json.dumps(dicc).encode('utf-8')
            conn.send(codigo_enviar)


            if solicitar == 1:
                msg = "solicito_aterrizaje"
                dicc = {"msg":msg, "list":codigo, "nro_vuelo":nro_vuelo}
                codigo_enviar = json.dumps(dicc).encode('utf-8')
                conn.send(codigo_enviar)
                solicitar = 0
                
            
            time.sleep(10)
    except:
        print("rtdc perdida")


def escuchar_PC(conn_PC, addr):
    global bloqueo_PC
    global dormido1
    estados = {"Piloto1":{"Somnolencia":0, "Pulso":0, "Hipoxia": 0,
                           "Muerte": 0, "Spo2": 0, "Bpm":0},
               "Piloto2":{"Somnolencia":0, "Pulso":0, "Hipoxia": 0,
                           "Muerte": 0, "Spo2": 0, "Bpm":0} }
    bloqueo_PC = 0
    while True:
        time.sleep(3)         
        if pin_on_off.value() == 1:
            pass
        else:
            message = conn_PC.recv(1024)
            print()
            print('Got a connection from PC %s' % str(addr)) 
            info_PC = json.loads(message.decode('utf-8'))               
            print(info_PC)

            if info_PC == "1":                
                if bloqueo_PC == 0:
                    bloqueo_PC = 1 
                elif bloqueo_PC == 1:
                    bloqueo_PC = 0
                                    
                if estados["Piloto1"]["Bpm"] != 0 and estados['Piloto1']["Spo2"] != 0:
                    bloqueo_PC = 1                                      
                    evaluar_info(estados["Piloto1"]["Bpm"],
                                  estados["Piloto1"]["Spo2"], 15, 1, "PC")
                else:
                    evaluar_info_piloto1(estados["Piloto1"])

                if estados["Piloto1"]["Somnolencia"] == '1':                                                 # Aunque use las bpm y spo2 si esta dormido se determina por esto
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

def evaluar_info_piloto1(info):
    global bpm_altos1, spo_bajos1, dormido1, muerte1
    if info["Pulso"] == '1':
        bpm_altos1 = 1
    else:
        bpm_altos1 = 0
    if info["Hipoxia"] == '1':
        spo_bajos1 = 1
    else:
        spo_bajos1 = 0
    if info["Muerte"] == '1':
        muerte1 = 1
    else:
        muerte1 = 0


alarma_sonora_1 = alarma_sonora_2 = info_aeropuerto = 0
def enviar_PC():
    global aterrizar, aterrizar_manual, solicitar, info_aeropuerto
    global alarma_sonora_1, alarma_sonora_2
    enviado = 0
    sonora1_enviada = 0
    sonora2_enviada = 0
    
    while True:
        # pedir permiso para aterrizar antes a rtdc

        if (aterrizar == 1 or aterrizar_manual == 1) and aterrizaje_enviado == 0:
            solicitar = 1
            print("aterrizar")                                   #------------------------------ UART
            aterrizaje_enviado = 1
                
        elif aterrizar_manual == 0 and aterrizar == 0 and aterrizaje_enviado == 1:
            print("no aterrizar")                                #------------------------------ UART
            aterrizaje_enviado = 0
                    

        if info_aeropuerto != 0:
            print("info aeropuerto", info_aeropuerto)            #------------------------------ UART
            info_aeropuerto = 0



        if alarma_sonora_1:
            print("prender alarma_sonora_1")                     #------------------------------ UART
            sonora1_enviada = 1
        elif not alarma_sonora_1 and sonora1_enviada:
            print("apagar alarma_sonora_1")                      #------------------------------ UART
            sonora1_enviada = 0
        
        if alarma_sonora_2:
            print("prender alarma_sonora_2")                     #------------------------------ UART
            sonora2_enviada = 1
        elif not alarma_sonora_2 and sonora2_enviada:
            print("apagar alarma_sonora_2")                      #------------------------------ UART
            sonora2_enviada = 0

        time.sleep(5)



bpm_bajos1 = bpm_altos1 = spo_bajos1 = dormido1 = temp_baja1 = temp_alta1 = muerte1 = 0 
bpm_bajos2 = bpm_altos2 = spo_bajos2 = dormido2 = temp_baja2 = temp_alta2 = muerte2 = 0
manual = no_reaccion = 0
pulsera_conectada = 1
intentional_loss = 0

pin_off = pin_on_off.value()
codigo = [
        bpm_altos1, bpm_altos2, 
        bpm_bajos1, bpm_bajos2, 
        dormido1, dormido2,
        spo_bajos1, spo_bajos2, 
        temp_alta1, temp_alta2, 
        temp_baja1, temp_baja2,
        muerte1, muerte2, 
        manual, pulsera_conectada,
        no_reaccion, pin_off
        ]


def actualizar_codigo():
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1, muerte1
    global bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2, muerte2 # se modifican directamente
    global manual, pulsera_conectada
    global codigo, no_reaccion, pin_on_off
    
    manual = pin_activacion_manual.value()
    pin_off = pin_on_off.value()
    codigo = [
              bpm_altos1, bpm_altos2, 
              bpm_bajos1, bpm_bajos2, 
              dormido1, dormido2,
              spo_bajos1, spo_bajos2, 
              temp_alta1, temp_alta2, 
              temp_baja1, temp_baja2,
              muerte1, muerte2, 
              manual, pulsera_conectada,
              no_reaccion, pin_off 
              ]
    return codigo


#para contador
pasaron_30segs_spo = pasaron_30segs_bpm = 0
contador_iniciado_60_bpm = contador_iniciado_60_spo = 0
contador_iniciado_30_bpm = contador_iniciado_30_spo = 0
alarmas_off_spo = alarmas_off_bpm = 0
            
t30spo = Timer(0)
t60spo = Timer(0)
t30bpm = Timer(0)
t60bpm = Timer(0)


def contador60spo(self):
    global alarmas_off_spo
    global contador_iniciado_60_spo
    contador_iniciado_60_spo = 0
    alarmas_off_spo = 0
def contador30spo(self):
    global alarmas_off_spo
    global pasaron_30segs_spo
    pasaron_30segs_spo = 1
    
    
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
    global alarmas_off_spo, alarmas_off_bpm
    global aterrizar, aterrizar_manual
    global alarma_sonora_1, alarma_sonora_2
    global no_reaccion, intentional_loss

    tocado = pin_reaccion.value()
    pin_boton_reaccion = 0
    ambar_titilando = ambar_prendido = 0
    prendido_roja = 0
    pin_on_off.value(0)
    while True:
        time.sleep(4)
        if pin_on_off.value() == 1:
            #pin_luz_ambar.value(0)
            #pin_luz_roja.value(0)
            print("pin on off maldito")
            pass
        else: 
            codigo = actualizar_codigo()
            print(codigo)
            print() 
            

            # Boton tipo switch
            # Si el boton de reaccion cambio de valor no va a valer lo que valia antes
            if pin_reaccion.value() != tocado:
                tocado = pin_reaccion.value()                       # Guarda el valor actual del pin
                pin_boton_reaccion = 1      # Pone en 1 la variable que se va a usar para saber si se presiono
                no_reaccion = 0      
                print("boton de reaccion")             

            #muerte 1 luz amarilla fija
            #2 muertos luz roja fija y sonido si por 30 segs no boton de reaccion  
            #avisa a rtdc emergencia 2 muertos


            # Protocolo hipoxia---------------------------------------------------------------------------------------------
            if codigo[6] or codigo[7]:                              # Si alguno tiene  hipoxia 
                if codigo[6] and codigo[7]:                         # Si ambos tienen  hipoxia 
                    print("2 spo")  
                    if alarmas_off_spo == 0:                        # Si las alarmas no estan desactivadas
                        alarma_sonora_1 = 1
                elif codigo[6] or codigo[7]:                        # Si solo 1 tiene
                    print("1 spo")
                    alarma_sonora_1 = 0
                                             
                if alarmas_off_spo == 0:                            # Si las alarmas no estan desactivadas
                    pin_luz_roja.value(1)                           # Activa luz alarma (hipoxia?
                    print("luz roja prendida alarmas off = 0")
                    roja_fija = 1 
                    
                    # Si el piloto toca el boton de reaccion desactiva las alarmas, no deja que tomen el control
                    # Tmb inicia un contador de 60segs que estara sin las alarmas
                    if pin_boton_reaccion == 1:                     # Si el boton de reaccion fue presionado
                        alarmas_off_spo = 1                         # Las alarmas de spo2 se desactivan
                        
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
                        no_reaccion = 1

                elif alarmas_off_spo == 1:                          # Sino si estan desactivadas las alarmas spo
                    pin_luz_roja.value(0)                           # Apaga luz alarma
                    print("luz roja apagada alarmas off = 1")
                    pass                                
                            
            elif not codigo[6] and not codigo[7]:                   # Si ninguno tiene spo2 en 1
                print("no spo")
                if not codigo[12] or not codigo[13]:                # Si uno no esta muerto
                    roja_fija = 0
                alarma_sonora_1 = 0          
            #---------------------------------------------------------------------------------------------

            #------------------------------------------
            
            #protocolo pulsaciones raras
            
            if codigo[0] or codigo[1] or codigo[2] or codigo[3]:   
                # Si cualquiera tiene bpm

                if codigo[0] and codigo[1] or codigo[2] and codigo[3] or codigo[0] and codigo[3] or codigo[1] and codigo[2]:
                    print("2 bpm")
                elif codigo[0] or codigo[1] or codigo[2] or codigo[3]:  
                    print("1 bpm")

                if alarmas_off_bpm == 0:                          # Si las alarmas no estan desactivadas
                    ambar_titilando = 1         # DEBERIA TITILAR
                    # Alarma sonora tmb

                    if pin_boton_reaccion == 1:                   # Si el boton esta presionado
                        alarmas_off_bpm = 1                       # DESACTIVA las alarmas                          
                        if contador_iniciado_60_bpm != 1:         # Si no esta iniciado el contador 60s
                            t60bpm.init(mode=Timer.ONE_SHOT, period=6000, callback=contador60bpm)
                            # INICIA temporizador, luego apagara la variable del contador 60s
                            # desactiva el apagado de las alarmas

                    elif contador_iniciado_30_bpm != 1:           # Sino, si no esta iniciado contador de 30s          
                        t30bpm.init(mode=Timer.ONE_SHOT, period=3000, callback=contador30bpm)
                        # INICIAtemporizador, luego apagara la variable del contador 30s
                        contador_iniciado_30_bpm = 1              # PRENDE variable del contador 30s
        
                    elif pasaron_30segs_bpm == 1:                 # Sino, si pasaron 30s
                        contador_iniciado_30_bpm = 0              # APAGA variable del contador iniciado 30s, porque ya paso
                        no_reaccion = 1                       # Deja que tomen el control
        
                elif alarmas_off_bpm == 1:                        # Sino, si estan apagadas las alarmas
                    ambar_titilando = 0 # DEBE DEJAR DE TITILAR
                    contador_iniciado_30_bpm = 0    
                    
                #alarma = 0
            elif not codigo[0] and not codigo[1] and not codigo[2] and not codigo[3]:   # Si ninguno tiene pulsaciones raras
                print("no bpm")
                ambar_titilando = 0
                #alarma = 0
            

            #-----------------------------------------

            if codigo[4] or codigo[5]:                  # Si esta dormido
                if ambar_titilando == 0:
                    pin_luz_ambar.value(1)   
                    print("luz ambar prendida dormidos sin titilar")                       
                    
                if codigo[4] and codigo[5]:             # Si son ambos
                    print("2 dormidos")
                    #   2dormidos hacer coso de 30 segs
                else:
                    print("1 dormido")
            else:
                print("0 dormidos")
                    
            #-----------------------------------------
            if pulsera_conectada == 0:                  # Si la pulsera esta desconectada
                if ambar_titilando == 0:                # Si no esta titilando    
                    pin_luz_ambar.value(1)
                    print("luz ambar prendida  pulsera desconectada y no titilando") 
                print("pulsera mal")
            else:
                print("pulsera bien")

            #-------------------------------------------------
            
            if codigo[12] and codigo[13]:               #si ambos estan muertos
                print("ambos muertos")
                pin_luz_roja.value(1)
                print("luz roja prendida 2 muertos")
                roja_fija = 1                           #roja no podra titilar
                ambar_fija = 0

            elif codigo[12] or codigo[13]:              #si solo 1 esta muerto
                print("uno muerto")
                pin_luz_ambar.value(1)
                print("luz ambar prendida 1 muerto") 
                ambar_fija = 1                          #ambar no podra titilar
                if not codigo[6] and not codigo[7]:      #si ninguno tiene hipoxia
                    roja_fija = 0
            else:
                if not codigo[6] or not codigo[7]:      
                    roja_fija = 0   
                ambar_fija = 0
                print("todos vivos")

            #-----------------------------------------------------
            #-----------------------------------------------------

            
            # Si no se cumple ninguna condicion para que la luz ambar este prendida entonces se apaga
            if ambar_titilando == 0:                                # Si no esta titilando
                if not codigo[4] and not codigo[5]:                 # Si ninguno esta dormido
                    if pulsera_conectada == 1:                      # Si la pulsera esta conectada
                        if not codigo[12] and not codigo[13] or codigo[12] and codigo[13]:  # Si ninguno o ambos estan muertos
                            if not codigo[0] and not codigo[1] and not codigo[2] and not codigo[3]: #si ninguno tiene pulsaciones
                                pin_luz_ambar.value(0)                          #SE APAGA
                                ambar_fija = 0
                                print("ambar apagada1")
            #------------------------------------------------------
            elif ambar_titilando == 1:                           # Si tiene que titilar
                if not ambar_fija:                               #si no esta fija
                    if ambar_prendido == 0:
                        pin_luz_ambar.value(1)
                        ambar_prendido = 1
                    elif ambar_prendido == 1:
                        pin_luz_ambar.value(0)
                        ambar_prendido = 0
                    print("ambar titilando")

            #---------------------------------------------------
            #---------------------------------------------------
            # Luz roja titilar 
            if codigo[14] or intentional_loss:              #cuando activacion manual o la rtdc lo indica
                aterrizar_manual = 1
                print("aterrizar manual = 1")
                if not roja_fija:
                    if prendido_roja == 0:
                        pin_luz_roja.value(1)
                        prendido_roja = 1
                    elif prendido_roja == 1:
                        pin_luz_roja.value(0)
                        prendido_roja = 0
                    print("roja titilando coso manual")
            else:                                           #si no esta la activacion manual ni intentional loss
                aterrizar_manual = 0    
                if not codigo[6] and not codigo[7]:         #si ninguno tiene hipoxia           
                    if not codigo[12] or not codigo[13]:       #si no estan muertos ambos
                        pin_luz_roja.value(0)           
                        print("luz roja apagada nada")                 

            pin_boton_reaccion = 0
                


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
print("Comunicación activada")

