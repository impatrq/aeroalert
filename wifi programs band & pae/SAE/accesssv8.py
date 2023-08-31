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

    global pin_luz_ambar, pin_luz_roja, pin_luz_test
    global pin_activacion_manual, pin_test, pin_reaccion, pin_on_off
    global pin_boton_activacion_manual, pin_boton_test, pin_boton_reaccion, pin_boton_on_off


    pin_luz_ambar = machine.Pin(23, machine.Pin.OUT)             
    pin_luz_roja = machine.Pin(5, machine.Pin.OUT)              
    pin_luz_test = machine.Pin(17, machine.Pin.OUT)                      
    
    pin_activacion_manual = machine.Pin(4, machine.Pin.IN)
    pin_boton_activacion_manual = pin_activacion_manual.value()

    pin_test = machine.Pin(25, machine.Pin.IN)                   
    pin_boton_test = pin_test.value()
    
    pin_reaccion = machine.Pin(33, machine.Pin.IN)
    pin_boton_reaccion = pin_reaccion.value()                
    
    pin_on_off = machine.Pin(35, machine.Pin.IN)             
    pin_boton_on_off = pin_on_off.value()

definir_pines()


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
    
    while True:
        print("Escuchando tipos")
        conn, addr = s.accept()
        print('Got a type connection from %s' % str(addr))
        message = conn.recv(1024)
        tipo = json.loads(message.decode('utf-8'))
        
        if tipo == "soy_band":
            _thread.start_new_thread(escuchar_band, (conn, addr))
           
        
        elif tipo == "soy_rtdc":
            _thread.start_new_thread(escuchar_rtdc, (conn, addr))
            _thread.start_new_thread(enviar_rtdc, (conn, addr))


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
        print("bpm={:02} spo={:02}% Temp={:02}°C puesta={:1}".format(bpm, spo, temp, conectado))
        evaluar_info(bpm, spo, temp, conectado, "band")    


def evaluar_info_piloto2():
    global bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2
    # Recibir por uart
    return

def recibir_uart():
    global uart
    global bloqueo_uart
    global dormido1
    while True:
        time.sleep(1)
        info_uart = uart.read()
        info_uart = {"Piloto":1, 
                     "Somnolencia": 'normal som', 
                     "Pulso":94, 
                     "Spo2":92, 
                     "bloqueo":1, 
                     "Muerte": 1,}
        
        print("uart recibido")
        
        if info_uart["piloto"] == 1:
            if info_uart["bloqueo"] == 1:
                bloqueo_uart = 1
            
                if info_uart["somnolencia"] == 1:
                    dormido1 = 1
                else:
                    dormido1 = 0
                evaluar_info(info_uart["bpms"], info_uart["spo"], 15, 1, "uart")
                
        
    # Read
    # uart.write()) # Read as much as possible using




bpm_bajos1 = bpm_altos1 = spo_bajos1 = dormido1 = temp_baja1 = temp_alta1 = 0 
bpm_bajos2 = bpm_altos2 = spo_bajos2 = dormido2 = temp_baja2 = temp_alta2 = 0
tomar_control = pin_boton_activacion_manual = 0
codigo = [
        bpm_altos1, bpm_altos2, 
        bpm_bajos1, bpm_bajos2, 
        dormido1, dormido2,
        spo_bajos1, spo_bajos2, 
        temp_alta1, temp_alta2, 
        temp_baja1, temp_baja2,
        tomar_control, manual]


def actualizar_codigo():
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1
    global bpm_bajos2, bpm_altos2, spo_bajos2, dormido2, temp_baja2, temp_alta2 # se modifican directamente
    global tomar_control, manual
    global codigo
    manual = pin_activacion_manual.value()
    codigo = [
              bpm_altos1, bpm_altos2, 
              bpm_bajos1, bpm_bajos2, 
              dormido1, dormido2,
              spo_bajos1, spo_bajos2, 
              temp_alta1, temp_alta2, 
              temp_baja1, temp_baja2,
              tomar_control, manual
              ]
    return codigo

def escuchar_rtdc(conn_rtdc,addr):
    while True:
        message = conn_rtdc.recv(1024)
        print('Got a connection from rtdc %s' % str(addr))
        data = json.loads(message.decode('utf-8'))
        # Recibe los comandos de vuelo enviados por la rtdc 
        # tipo "ATERRIZA" "BLOQUEAR"
        # HAY QUE EVALUAR ESTA INFORMACION Y MANDAR LO CORRESPONDIENTE AL XPLANE   

def enviar_rtdc(conn, addr):
    global codigo
    while True:
        print("enviando a RTDC: ", addr)
        codigo = actualizar_codigo()
        codigo_enviar = json.dumps(codigo).encode('utf-8')
        conn.send(codigo_enviar)
        time.sleep(10)
        



#para contador
pasaron_30segs_spo = pasaron_30segs_bpm = 0
contador_iniciado_60_bpm = contador_iniciado_60_spo = 0
contador_iniciado_30_bpm = contador_iniciado_30_spo = 0
tomar_control = alarmas_off_spo = alarmas_off_bpm = 0
            
t30spo = Timer(0)
t60spo = Timer(0)
t30bpm = Timer(0)
t60bpm = Timer(0)


def contador(cual):
    global alarmas_off_bpm
    global alarmas_off_spo

    #despues de que pase el tiempo del timer se va a hacer la accion segun el arg ("cual")
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
        contador_iniciado_60_bpm = 0
        alarmas_off_bpm = 0



def activar_SAE():
    time.sleep(1)
    global codigo
    global pasaron_30segs_spo, pasaron_30segs_bpm
    global contador_iniciado_60_bpm, contador_iniciado_60_spo
    global contador_iniciado_30_bpm, contador_iniciado_30_spo
    global tomar_control, alarmas_off_spo, alarmas_off_bpm
    tocado = pin_reaccion.value()
    pin_boton_reaccion = 0
    ambar_titilando = 0
    #------------------------------------------
    
    while True:
        time.sleep(1)
        codigo = actualizar_codigo()
        print(codigo)
        print()
        

        if ambar_titilando == 1:
            if pin_luz_ambar.value() == 0:
                pin_luz_ambar.value(1)
            else:
                pin_luz_ambar.value(0)
        elif ambar_titilando == 0:
            pin_luz_ambar.value(0)


        # Luz roja titilar cuando activacion manual
        if pin_activacion_manual == 1:
            if prendido == 0:
                pin_luz_roja.value(1)
                prendido = 1
            elif prendido == 1:
                pin_luz_roja.value(0)
                prendido = 0

        # Boton tipo switch
        # Si el boton de reaccion cambio de valor no va a valer lo que valia antes
        if pin_reaccion.value() != tocado:
            tocado = pin_reaccion.value()                       # Guarda el valor actual del pin
            pin_boton_reaccion = 1                              # Pone en 1 la variable que se va a usar para saber si se presiono
            

        # Protocolo hipoxia
        if codigo[6] and codigo[7]:                       # Si ambos tienen 6 y 7 activos (hipoxia)

            if alarmas_off_spo == 0:                            # Si las alarmas no estan desactivadas
                pin_luz_roja.value(1)                           # Activa luz alarma (hipoxia?
                # Alarma sonora tmb deberia

                # Si el piloto toca el boton de reaccion desactiva las alarmas, no deja que tomen el control
                # Tmb inicia un contador de 60segs que estara sin las alarmas
                if pin_boton_reaccion == 1:                     # Si el boton de reaccion fue presionado
                    alarmas_off_spo = 1                         # Las alarmas de spo2 se desactivan
                    tomar_control = 0                           # Se pone en 0 el pin de tomar el control
                    if contador_iniciado_60_spo != 1:           # Si el contador de 60s spo2 no esta iniciado
                        t60spo.init(mode=Timer.ONE_SHOT, period=60000, callback=contador, args="60spo") #Lo inicia
                        contador_iniciado_60_spo = 1            # Cambia la variable para que la prox sepa que esta activado


                # Inicia contador 30 segs para definir hipoxia peligrosa
                elif contador_iniciado_30_spo != 1:             # Sino si el contador de 30s spo2 no esta iniciado
                    t30spo.init(mode=Timer.ONE_SHOT, period=30000, callback=contador, args="30spo")
                    contador_iniciado_30_spo = 1                # Pone la variable en 1  cont_init_30spo


                # 30 segs despues de tener hipoxia y no tener reaccion deja que tomen el control
                elif pasaron_30segs_spo == 1:                   # Sino si pasaron30segsspo2 esta en 1
                    contador_iniciado_30_spo = 0                # Pone en 0 la variable de cont_init_30spo
                    if pin_boton_reaccion != 1:                 # Si el pin de reaccion no es 1
                        tomar_control = 1                       # Pone pin tomar control en 1


            elif alarmas_off_spo == 1:                          # Sino si estan desactivadas las alarmas spo
                pin_luz_roja.value(0)                           # Apaga luz alarma
                pass        

        elif codigo[6] or codigo[7]:                      # Sino si 1 tiene spo2 en 1
            print("1 piloto tiene hipoxia")     
            pin_luz_roja.value(1)                               # No se si sea la luz roja de todos modos
            # Apagar alarma sonora      
        elif not codigo[6] and not codigo[7]:                     # Sino si ninguno tiene spo2 en 1
            print("ningun piloto tiene hipoxia")
            pin_luz_roja.value(0)
            


        #------------------------------------------
        

        #codigo 0 pulsaciones altas piloto 1
        #codigo 1 pulsaciones altas piloto 2
        #codigo 2 pulsaciones bajas piloto 1
        #codigo 3 pulsaciones bajas piloto 2
        
        #protocolo pulsaciones raras
        if codigo[0] and codigo[1] or codigo[2] and codigo[3] or codigo[0] and codigo[3] or codigo[1] and codigo[2]:                       # Si ambos tienen    
            if alarmas_off_bpm != 1:                          # Si las alarmas no estan desactivadas
                pin_luz_ambar.value(1)                          # DEBERIA TITILAR
                ambar_titilando = 1

                # Alarma sonora tmb

                if pin_boton_reaccion == 1:                     # Si el boton esta presionado
                    alarmas_off_bpm = 1                       # DESACTIVA las alarmas
                    tomar_control = 0                           # No permite que tomen el control
                    if contador_iniciado_60_bpm != 1:         # Si no esta iniciado el contador 60s
                        t60bpm.init(mode=Timer.ONE_SHOT, period=6000, callback=contador, args="60bpm")
                                                                # INICIA temporizador, luego apagara la variable del contador 60s
                        contador_iniciado_60_bpm = 1          # PRENDE variable del contador 60s

                elif contador_iniciado_30_bpm != 1:           # Sino, si no esta iniciado contador de 30s          
                    t30bpm.init(mode=Timer.ONE_SHOT, period=3000, callback=contador, args="30bpm")
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
            print("pulsaciones raras 1 piloto") 
            pin_luz_ambar.value(1)                              # DEBERIA TITILAR
            ambar_titilando = 1 
        elif not codigo[0] and not codigo[1] and not codigo[2] and not codigo[3]:          # Si ninguno tiene pulsaciones raras
            print("ninguno de los 2 pilotos tine pulsaciones raras")
            pin_luz_ambar.value(0)                              # DEBE DEJAR DE TITILAR
            ambar_titilando = 0
        
        
        #------------------------------------------
        if ambar_titilando != 1:                                # Si no esta titilando
            if dormido1 == 1:   
                pin_luz_ambar.value(1)                          # SIN TITILAR
                print("el piloto esta dormido") 
            else:   
                pin_luz_ambar.value(0)                          #SE APAGA
                print("el piloto esta despierto")

        if pin_boton_reaccion == 1:
            pin_boton_reaccion = 0





listabpm = []
listaspo = []
def evaluar_info(bpm, spo, temp, conectado, de):
    global bpm_bajos1, bpm_altos1, spo_bajos1, dormido1, temp_baja1, temp_alta1
    global listabpm, listaspo
    global bloqueo_uart

    if bloqueo_uart == 0 or de == "uart":
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
print("wifi conectado")

_thread.start_new_thread(activar_SAE, ())
print("protocolos activados")
time.sleep(1)



uart = UART(1, 115200) # 1st argument: UART number: Hardware UART #1
_thread.start_new_thread(recibir_uart, ())
time.sleep(1)
print("uart activado")



_thread.start_new_thread(escuchar_tipos, ())
print("captar rtdc y band activado")


#_thread.start_new_thread(recibir_band2, (station3,))
#exchange_data2(station2)
#exchange_data1(station1)
