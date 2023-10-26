import usocket as socket
import gc                                                                               #import esp
gc.collect()                                                                            #esp.osdebug(None)
import time, json, _thread
import network
from machine import Pin, Timer, UART



def definir_pines():
    global pin_luz_ambar, pin_luz_roja, pin_flag
    global pin_activacion_manual, pin_test, pin_reaccion, pin_on_off
    global pin_boton_test, pin_boton_reaccion

    pin_luz_roja = Pin(4, Pin.OUT)              
    pin_luz_ambar = Pin(17, Pin.OUT)                         
    pin_flag = Pin(26, Pin.OUT)               
    pin_activacion_manual = Pin(22, Pin.IN)


    pin_test = Pin(18, Pin.IN)                   
    pin_boton_test = pin_test.value()
    pin_reaccion = Pin(19, Pin.IN)
    pin_boton_reaccion = pin_reaccion.value()
    pin_on_off = Pin(35, Pin.IN)
    # 4 17 18 19 21 35
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

aterrizar_rtdc = 0
info_aeropuerto = 0
def escuchar_rtdc(conn_rtdc,addr):
    global aterrizar_rtdc, intentional_loss, info_aeropuerto
    pin_flag.value(0)
    try:
        while True:
            data = conn_rtdc.recv(1024)
            message = json.loads(data.decode('utf-8'))
            print('From RTDC %s' % str(addr))
            print(message)

            if message['mensaje'] == "aterriza":
                print("tiene que aterrizar")                        #ATERRIZAR ATERRIZAR ATERRIZAR ATERRIZAR 
                aterrizar_rtdc = 1                                                
            elif message['mensaje'] == "no aterrizes":
                print("no tiene que aterrizar")
                aterrizar_rtdc = 0

            elif message['mensaje'] == type(dict):
                info_aeropuerto = message['mensaje']['info aeropuerto']             #msg = {'mensaje':{'info aeropuerto':{'nombre':ezeiza, 'coordenadas':"213123131231"}}

            elif message['mensaje'] == "intentional loss":
                intentional_loss = 1
            elif message['mensaje'] == "apagar intentional loss":
                intentional_loss = 0
                
    except:
        pin_flag.value(1)
        #si no se conecta la rtdc flag prendido
        # Recibe los comandos de vuelo enviados por la rtdc 


def enviar_rtdc(conn, addr):
    global solicitar, pin_on_off
    alerta_sae_enviada = 0
    nro_vuelo = 7365458
    try:
        while True:
            print("enviando a RTDC: ", addr)
            msg = ""

            if pin_on_off.value() == 1 and alerta_sae_enviada == 0:
                msg = "alerta_desactivacion_sae"
                alerta_sae_enviada = 1
            elif pin_on_off.value() == 0 and alerta_sae_enviada == 1:
                msg = "sae_activado"                
                alerta_sae_enviada = 0

            if msg != "":
                codigo = actualizar_codigo()
                dicc = {"msg":msg, "list":codigo, "nro_vuelo":nro_vuelo}
                codigo_enviar = json.dumps(dicc).encode('utf-8')
                conn.send(codigo_enviar)


            if solicitar == 1:
                msg = "solicito_aterrizaje"
                codigo = actualizar_codigo()
                dicc = {"msg":msg, "list":codigo, "nro_vuelo":nro_vuelo}
                codigo_enviar = json.dumps(dicc).encode('utf-8')
                conn.send(codigo_enviar)
                solicitar = 0
                    
            
            time.sleep(5)
    except:
        print("rtdc perdida")


bloqueo_PC = 0
def escuchar_PC(conn_PC, addr):
    global bloqueo_PC
    global dormido1
    estados = {"Piloto1":{"Somnolencia":0, "Pulso":0, "Hipoxia": 0,
                           "Muerte": 0, "Spo2": 0, "Bpm":0},
               "Piloto2":{"Somnolencia":0, "Pulso":0, "Hipoxia": 0,
                           "Muerte": 0, "Spo2": 0, "Bpm":0}}
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
                                    
                if estados["Piloto1"]["Bpm"] > 0.5 and estados['Piloto1']["Spo2"] > 0.5:
                    bloqueo_PC = 1                                      
                    evaluar_info(estados["Piloto1"]["Bpm"],
                                  estados["Piloto1"]["Spo2"], 15, 1, "PC")
                else:
                    evaluar_info_piloto1(estados["Piloto1"])
                    bloqueo_PC = 0

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
    global bpm_altos1, spo_bajos1, muerte1
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



bpm_bajos1 = bpm_altos1 = spo_bajos1 = dormido1 = temp_baja1 = temp_alta1 = muerte1 = 0 
bpm_bajos2 = bpm_altos2 = spo_bajos2 = dormido2 = temp_baja2 = temp_alta2 = muerte2 = 0
manual = no_reaccion = 0
pulsera_conectada = 1
intentional_loss = 0

pin_off = pin_on_off.value()
codigo = [
            bpm_altos1,     bpm_altos2,             # 0,1
            bpm_bajos1,     bpm_bajos2,             # 2,3
            dormido1  ,     dormido2,               # 4,5
            spo_bajos1,     spo_bajos2,             # 6,7
            temp_alta1,     temp_alta2,             # 8,9
            temp_baja1,     temp_baja2,             # 10,11
            muerte1   ,     muerte2,                # 12,13
            manual    ,     pulsera_conectada,      # 14,15
            no_reaccion,     pin_off                # 16,17
            ]


def actualizar_codigo():
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1, muerte1
    global bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2, muerte2 # se modifican directamente
    global manual, pulsera_conectada
    global no_reaccion, pin_on_off
    
    manual = pin_activacion_manual.value()
    pin_off = pin_on_off.value()
    codigo = [
                bpm_altos1,     bpm_altos2,             # 0,1
                bpm_bajos1,     bpm_bajos2,             # 2,3
                dormido1  ,     dormido2,               # 4,5
                spo_bajos1,     spo_bajos2,             # 6,7
                temp_alta1,     temp_alta2,             # 8,9
                temp_baja1,     temp_baja2,             # 10,11
                muerte1   ,     muerte2,                # 12,13
                manual    ,     pulsera_conectada,      # 14,15
                no_reaccion,     pin_off                # 16,17
                ]
    return codigo


#para contador


t30 = Timer(0)
t60 = Timer(0)

alarmas_off= pasaron_30segs = 0
def contador60(self):
    global alarmas_off
    alarmas_off = 0

def contador30(self):
    global pasaron_30segs
    pasaron_30segs = 1
    
def activar_SAE():
    time.sleep(1)
    global pulsera_conectada
    global solicitar, info_aeropuerto
    global no_reaccion, intentional_loss
    global pin_boton_test

    pin_boton_reaccion = 0

    hipoxia1 = hipoxia2 = bpm1 = bpm2 = asleep1 = asleep2 = muertos1 = muertos2 = 0 

    roja_fija = roja_titilando = prendido_roja = 0
    ambar_fija = ambar_titilando = prendido_ambar = 0

    #bien
    alarma_hipoxia = enviado_alarma_hipoxia = 0
    alarma_aes = enviado_alarma_aes = 0
    alarma_dormidos = enviado_alarma_dormidos = 0
    alarma_manual_activation = enviado_manual_activation = 0
    alarma_aes_activation = enviado_aes_activation = 0
    #--------------

    while True:
        time.sleep(4)
        print()
        
        if pin_reaccion.value():
            pin_boton_reaccion = 1      # Pone en 1 la variable que se va a usar para saber si se presiono
            no_reaccion = 0      
            print("boton de reaccion")    

        codigo = actualizar_codigo()
        print(codigo)
        print() 
    
        if pin_on_off.value() == 1:
            print("pin on off")
            pin_flag.value(1)
            pin_luz_ambar.value(0)
            pin_luz_roja.value(0)
            if enviado_alarma_hipoxia:
                print("alarma_hipoxia=0")
                enviado_alarma_hipoxia = 0
            if enviado_alarma_aes:
                print("alarma_aes_alert=0")
                enviado_alarma_aes = 0
            if enviado_alarma_dormidos:
                print("alarma_dormidos=0")
                enviado_alarma_dormidos = 0
            if enviado_manual_activation:
                print("alarma_manual_activation=0")
                enviado_manual_activation = 0
            if enviado_aes_activation:
                print("alarma_aes_activation=0")
                enviado_aes_activation = 0

        else: 
            pin_flag.value(0)

            #determinacion muertos
            if codigo[12] and codigo[13]:
                muertos2 = 1
                muertos1 = 0
                print("2Muertos")
            elif codigo[12] or codigo[13]:
                muertos1 = 1
                muertos2 = 0
                print("1Muerto")
            else:
                muertos2 = 0
                muertos1 = 0
                print("no Muertos")


            #determinacion dormidos
            if codigo[4] and codigo[5]:                             # si ambos estan dormidos
                asleep2 = 1
                asleep1 = 0
                print("2Dormidos")
            elif codigo[4] or codigo[5]:                              # si solo 1 esta dormido
                asleep1 = 1
                asleep2 = 0
                print("1Dormido")
            else:
                asleep1 = 0
                asleep2 = 0
                print("no Dormidos")
                

            # Protocolo alarmas off---------------------------------------------------------------------------------------------
                #hipoxia______________      #bpms_____________________________________________     #dormidos____________
            if (codigo[6] or codigo[7]) or (codigo[0] or codigo[1] or codigo[2] or codigo[3]) or (codigo[4] and codigo[5]):  # Si alguno tiene spo o bpms o estan dormidos ambos
                 
                if codigo[6] and codigo[7]:                         # Si ambos tienen  hipoxia 
                    hipoxia2 = 1 
                    hipoxia1 = 0
                    print("2Spo")
                elif codigo[6] or codigo[7]:                        # Si solo 1 tiene
                    hipoxia1 = 1
                    hipoxia2 = 0
                    print("1Spo") 
                else:
                    hipoxia1 = 0
                    hipoxia2 = 0
                    print("no Spo")

                if (codigo[0] and codigo[1]) or (codigo[2] and codigo[3]) or (codigo[0] and codigo[3]) or (codigo[1] and codigo[2]):
                    bpm2 = 1
                    bpm1 = 0
                    print("2Bpm")
                elif codigo[0] or codigo[1] or codigo[2] or codigo[3]:  
                    bpm1 = 1
                    bpm2 = 0
                    print("1Bpm")
                else:
                    bpm1 = 0
                    bpm2 = 0
                    print("no Bpm")


                #------------------------------------------------------------------------------------------
                if alarmas_off == 0:                                    # Si las alarmas no estan desactivadas
                    # Si el piloto toca el boton de reaccion desactiva las alarmas
                    if pin_boton_reaccion == 1:                         # Si el boton de reaccion fue presionado
                        alarmas_off = 1                                 # Las alarmas de  se desactivan
                        t60.init(mode=Timer.ONE_SHOT, period=60000, callback=contador60) 
                        pasaron_30segs = 0
                        #dentro de 60 segs se pone alarmas off spo en 0 de nuevo

                    # Inicia contador 30 segs para definir alerta peligrosa
                    elif contador_iniciado_30 == 0:                     # Sino si el contador de 30s  no esta iniciado
                        t30.init(mode=Timer.ONE_SHOT, period=30000, callback=contador30)
                        contador_iniciado_30 = 1                        # Pone la variable en 1  cont_init_30

                    # 30 segs despues y no tener reaccion es una alerta alta
                    elif pasaron_30segs == 1:                           # Sino si pasaron30segs esta en 1
                        contador_iniciado_30 = 0                        # Pone en 0 la variable de cont_init_30spo
                        no_reaccion = 1
                        pasaron_30segs = 0
                        print("no reacciono")


                elif alarmas_off == 1:                                  # Sino si estan desactivadas las alarmas spo
                    print("alarmas off")
                    pasaron_30segs = 0
                    #
                    # enviar UART para apagar alarmas sonoras
                    #
            else:
                hipoxia1 = hipoxia2 = bpm1 = bpm2 = asleep1 = asleep2 = 0                                     
        

            #---------------------------------------------------------------------------------------------

            # 1 o 2 spo                 Roja Fija                       alarma sonora hipoxiaa          -
            #                                                           
            #   
            # 2 muertos                 Roja Fija                       alarma_sonora_aes_alert         -
            # 1 muerto                  Ambar Fija                      alarma_sonora_aes_alert
            #                                                           
            #
            # 1 o 2 bpm                 Ambar Titilar                   alarma_sonora_aes_alert         -
            #                                                           
            # 
            # 1 o 2 dormidos            Ambar Fija                      alarma_sonora_dormidos
            #
            #                                                   
            # pulsera_conectada = 0     Ambar Fija
            #
            #                                                           
            # intentional loss          Roja Titilando                  alarma_sonora_aes_activation 
            # activacion manual         Roja Titilando                  alarma_sonora_manual_activation
            # 
            # 
            # test fail                                                 alarma_sonora_test_failed
            # test pass                                                 alarma_sonora_test_passed
            # 
            # 
            #-------------------------------------------------------------------------------
            if hipoxia1 or hipoxia2:                    #si uno o 2 tienen
                roja_fija = 1
                alarma_hipoxia = 1
            else:
                alarma_hipoxia = 0

                
            if muertos1 or muertos2:
                alarma_aes= 1
                if muertos2:
                    roja_fija = 1

                elif muertos1:
                    ambar_fija = 1

            if not hipoxia1 and not hipoxia2 and not muertos2:
                roja_fija = 0



            if bpm1 or bpm2:
                ambar_titilando = 1
                alarma_aes = 1
            else:
                ambar_titilando = 0
            
            if not muertos1 and not muertos2 and not bpm1 and not bpm2:
                alarma_aes = 0

            if asleep1 or asleep2: 
                ambar_fija = 1
                alarma_dormidos = 1
            else:
                alarma_dormidos = 0

            if not pulsera_conectada:
                print("pulsera desconectada")
                ambar_fija = 1
            else:
                print("pulserac conectada")

            if not muertos1 and not asleep1 and not asleep2 and pulsera_conectada:
                ambar_fija = 0

                
            if codigo[14] or intentional_loss:              #activacion manual o intentional loss
                roja_titilando = 1
            else:
                roja_titilando = 0
            
            if codigo[14]:
                alarma_manual_activation = 1
                aterrizar = 1                               #aterrizar
            else:
                alarma_manual_activation = 0
                aterrizar = 0

            if intentional_loss or no_reaccion:
                alarma_aes_activation = 1
            else:
                alarma_aes_activation = 0

            #------------------------------------------------------------

            if alarmas_off == 0:                    #si no estan apagadas las alarmas

                #luz roja  
                if roja_fija:
                    pin_luz_roja.value(1)
                    prendido_roja = 1
                else:
                    if roja_titilando:
                        if prendido_roja:
                            pin_luz_roja.value(0)
                            prendido_roja = 0
                        else:
                            pin_luz_roja.value(1)
                            prendido_roja = 1
                    else:
                        pin_luz_roja.value(0)
                        prendido_roja = 0
                
                #luz ambar
                if ambar_fija:
                    pin_luz_ambar.value(1)
                    prendido_ambar = 1
                else:
                    if ambar_titilando:
                        if prendido_ambar:
                            pin_luz_ambar.value(0)
                            prendido_ambar = 0
                        else:
                            pin_luz_ambar.value(1)
                            prendido_ambar = 1
                    else:
                        pin_luz_ambar.value(0)
                        prendido_ambar = 0
                        
                #-----------------------------------------------------------

                if alarma_hipoxia and not enviado_alarma_hipoxia:
                    print("alarma_hipoxia=1")
                    enviado_alarma_hipoxia = 1            
                elif enviado_alarma_hipoxia:
                    print("alarma_hipoxia=0")
                    enviado_alarma_hipoxia = 0
                
                if alarma_aes and not enviado_alarma_aes:
                    print("alarma_aes_alert=1")
                    enviado_alarma_aes = 1
                elif enviado_alarma_aes:
                    print("alarma_aes_alert=0")
                    enviado_alarma_aes = 0

                if alarma_dormidos and not enviado_alarma_dormidos:
                    print("alarma_dormidos=1")
                    enviado_alarma_dormidos = 1
                elif enviado_alarma_dormidos:
                    print("alarma_dormidos=0")
                    enviado_alarma_dormidos = 0

                if alarma_manual_activation and not enviado_manual_activation:
                    print("alarma_manual_activation=1")
                    enviado_manual_activation = 1
                elif enviado_manual_activation:
                    print("alarma_manual_activation=0")
                    enviado_manual_activation = 0

                if alarma_aes_activation and not enviado_aes_activation:
                    print("alarma_aes_activation=1")
                    enviado_aes_activation = 1
                elif enviado_aes_activation:
                    print("alarma_aes_activation=0")
                    enviado_aes_activation = 0

                # faltan los 2 de test, pass y fail

            else:                                       #si estan apagadas las alarmas
                pin_luz_ambar.value(0)
                pin_luz_roja.value(0)
                if enviado_alarma_hipoxia:
                    print("alarma_hipoxia=0")
                    enviado_alarma_hipoxia = 0
                if enviado_alarma_aes:
                    print("alarma_aes_alert=0")
                    enviado_alarma_aes = 0
                if enviado_alarma_dormidos:
                    print("alarma_dormidos=0")
                    enviado_alarma_dormidos = 0
                if enviado_manual_activation:
                    print("alarma_manual_activation=0")
                    enviado_manual_activation = 0
                if enviado_aes_activation:
                    print("alarma_aes_activation=0")
                    enviado_aes_activation = 0
            

        #-----------------------------------------------------
        # sin depender de alarmas off nidel pin on-off
        if ((aterrizar and pin_on_off == 0) or intentional_loss) and not aterrizaje_enviado:
            solicitar = 1
            print("aterrizar")
            aterrizaje_enviado = 1
        elif not aterrizar and not intentional_loss and aterrizaje_enviado:
            solicitar = 0
            print("no aterrizar")
            aterrizaje_enviado = 0

        if info_aeropuerto != 0:
            print("info aeropuerto:", info_aeropuerto)            
            info_aeropuerto = 0


        pin_boton_reaccion = 0


        if pin_test.value() != pin_boton_test:
            pin_boton_test = pin_test.value()

            print("pin_test prendido, analizando")
            pin_luz_ambar.value(1)
            pin_luz_roja.value(1)
            pin_flag.value(1)
            time.sleep(5)
            pin_luz_ambar.value(0)
            pin_luz_roja.value(0)
            pin_flag.value(0)


listabpm = []
listaspo = []
def evaluar_info(bpm, spo, temp, conectado, de):
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1, muerte1
    global listabpm, listaspo           #se usa en distintos threads por eso global
    global bloqueo_PC
    global pulsera_conectada

    if bloqueo_PC == 0:          # se evalua la info si es de band /sin bloqueo
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
        elif bpm > 130:
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

    