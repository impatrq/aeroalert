import stationctrt as stationctrt
from machine import Pin
from time import sleep
import time
hora = time.localtime()



global client_socket, sta_if

client_socket, sta_if = stationctrt.do_connect()
print(client_socket, sta_if)
#stationctrt.send_type(client_socket, "soy_ctrt")


pin_luz_roja = Pin(21, Pin.OUT)
pin_luz_ambar = Pin(19, Pin.OUT)



# Defininicón de Pines keypad
filas = [33, 32, 12, 13]
columnas = [14, 27, 26, 25]
# Definimos los pines de las filas como salida
pines_Filas = [Pin(pin_nombre, mode=Pin.OUT) for pin_nombre in filas]
# Definimos los pines de las columnas de salida
pines_Columnas = [Pin(pin_nombre, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_nombre in columnas]



alert = emergency = solicitud = sae_desactivado = 0

#informacion de aeropuertos
info_aeropuertos = {'airports':
                               [
                                {"nombre":"Ezeiza", "coordenadas": ["34°49′25″, 58°31′44″"]},
                                {"nombre":"Aeroparque", "coordenadas": ["34°33'27″ 58°24'43″"]},
                                {"nombre":"Ambrosio Taravella", "coordenadas": ["31°19'03″ 64°12'36″"]},
                                {"nombre":"Moron", "coordenadas": ["33°29'13″ 54°52'26″"]},
                                {"nombre":"Quilmes", "coordenadas": ["35°34'17″ 57°54'45″"]}
                               ]
                   }

nombres_variables = {"variables":
                     ["Hour","BpmH1","BpmH2","BpmL1","BpmL2","Sle1","Sle2",
                    "Oxi1","Oxi2","C°H1","C°H2","C°L1","C°L2",
                    "Death1","Death2","Manual","BandCable","NoReact", "Off"]}

historial_de_vuelos = {'12323': {'datos con hora': [
                                                      ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                                                      ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                                                   ], 
                                   'alertas': {'alert': 0, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 0}
                                   },
                        '5643': {'datos con hora': [
                                                      ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                                                      ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                                                      ], 
                                   'alertas': {'alert': 0, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 0}
                                 },
                       '4321': {'datos con hora': [
                                                      ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                                                      ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                                      ['10:18:36', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                                      ['10:18:37', 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                                      ['10:18:38', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                                                      ], 
                                   'alertas': {'alert': 0, 'emergency': 0, 'solicitud': 0, 'sae_desactivado': 0}
                                 }
                         }


def notification(cual, nro_vuelo, data):
    #Protocolos dentro de la pestaña de la CTRT
    global pin_luz_ambar, pin_luz_roja
    global alert, emergency, solicitud, sae_desactivado
    global historial_de_vuelos

    if cual == "emergency":
        print("emergency")
        pin_luz_roja.value(1)
        pin_luz_ambar.value(0)
        emergency = 1
        alert = 0
    elif cual == "alert":
        print("alert")
        pin_luz_roja.value(0)
        pin_luz_ambar.value(1)
        alert = 1
        emergency = 0
    elif cual == "clean":
        pin_luz_ambar.value(0)
        pin_luz_roja.value(0)
        alert = 0
        emergency = 0
    


    vuelo_nro = str(nro_vuelo)

    hora = time.localtime()
    hora_string = str("%02.0f:%02.0f:%02.0f" %(hora[3],hora[4],hora[5]))

    info_hora = [hora_string]
    for i in data:  
        info_hora.append(i)
    #info_hora = ["23:23:43",0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]



    alerts = {"alert": alert, "emergency": emergency, "solicitud": solicitud, "sae_desactivado": sae_desactivado}


    if vuelo_nro in historial_de_vuelos:
        historial_de_vuelos[vuelo_nro]["datos con hora"].append(info_hora)
        historial_de_vuelos[vuelo_nro]["datos con hora"] = historial_de_vuelos[vuelo_nro]["datos con hora"][-20:]
        #maximo 20 datos con hora
        historial_de_vuelos[vuelo_nro]["alertas"] = alerts
    else:
        historial_de_vuelos[vuelo_nro] = {"datos con hora":[info_hora],"alertas":alerts}

        #historial_de_vuelos = 
        #{'12323': {'datos con hora': [
        #                              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
        #                              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        #                              ], 
        #           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}
        #           },
        #'5643': {'datos con hora': [
        #                              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
        #                              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        #                              ], 
        #           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}
        #         }
        # }



def manage_AES():
    global solicitud, sae_desactivado
    errores = 0
    while True:
        try:
            recibido = stationctrt.receive_data(client_socket)
            #recibido = {"msg":"solicito: aterrizaje", "nro_vuelo": 4334, "list": (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)}
            print("\nrecibido aes: ", recibido)

            msg = recibido["msg"]                   #puede ser ""
            nro_vuelo = recibido["nro_vuelo"]
            data = recibido["list"]                     

            if msg == "solicito_aterrizaje":
                solicitud = 1        
            elif msg == "alerta_desactivacion_sae":
                sae_desactivado = 1
            elif msg == "sae_activado":
                sae_desactivado = 0

            #Info
            I={"bpm_altos1": data[0],         "bpm_altos2": data[1], 
                "bpm_bajos1": data[2],         "bpm_bajos2": data[3], 
                "dormido1": data[4],           "dormido2": data[5],
                "spo_bajos1": data[6],         "spo_bajos2": data[7], 
                "temp_alta1": data[8],         "temp_alta2": data[9], 
                "temp_baja1": data[10],        "temp_baja2": data[11],
                "muerte1": data[12],           "muerte2": data[13], 
                "manual": data[14], "pulsera_conectada": data[15],
                "no_reaccion": data[16],        "pin_on_off": data[17]}
            
            if I["no_reaccion"] or I["manual"] or (I["muerte1"] and I["muerte2"]):
                notification("emergency",nro_vuelo, data)
            
            elif I["muerte1"] or I["muerte2"] or I["spo_bajos1"] or I["spo_bajos2"] or I["dormido1"] or I["dormido2"] or not I["pulsera_conectada"] or I["pin_on_off"]:
                notification("alert",nro_vuelo,  data)

            elif sae_desactivado == 1:
                notification("alert",nro_vuelo, data)
                
            if sum(data) == 1 and I["pulsera_conectada"] == 1:
                notification("clean",nro_vuelo, data)
        except Exception as error:
            errores +=1
            print("fallo:", error)
            time.sleep(1)



def inicio():
    #Función para inicializar el teclado
    for fila in range(0,4):
        for col in range(0,4):
            pines_Filas[fila].value(0)

# Constantes
Tecla_Arriba = 0
Tecla_Abajo = 1
def escanear(fila, columna):
    """ Escaneo del teclado """

    # poner todas las filas en alto
    pines_Filas[fila].value(1)
    key = None

    # verificación al presionar una tecla o evento
    if pines_Columnas [columna].value() == Tecla_Abajo:
        key = Tecla_Abajo
    if pines_Columnas [columna].value() == Tecla_Arriba:
        key = Tecla_Arriba
    pines_Filas [fila].value(0)

    # retorne el estado de la tecla
    return key

def teclas():
    # poner todas las columnas en bajo
    inicio()

    teclas = [['1', '4', '7', '*'], ['2', '5', '8', '0'], ['3', '6', '9', '#'], ['A', 'B', 'C', 'D']]
    
    #  * # A B C D
    # enter, arriba, abajo, deseleccionar
    #  D = softreset() 

    global last_key_press
    last_key_press = ""
    while True:
        for fila in range(4):
            for columna in range(4):
                tecla = escanear(fila, columna)
                if tecla == Tecla_Abajo:
                    #print("Es el numero: ", teclas[fila][columna])
                    last_key_press = teclas[fila][columna]
                    sleep(1)
                    last_key_press = ""


print("Importando microdot...")
from microdot import Microdot, send_file
print("Done")
import ujson
import _thread
#Programación de microdot para subir los datos a la pagina
def conectar_microdot():
    app = Microdot()

    @app.route('/')
    def index(request):
        print("\nEnviando index.html")
        return send_file("/assets/html/index.html")

    @app.route("/assets/<dir>/<file>")
    def assets(request, dir, file):
        """
        sirve para que el archivo html pueda usar los archivos dentro de la esp32, los solicita con el src='assets/js/code.js'

        Funcion asociada a una ruta que solicita archivos CSS o JS
        request (Request): Objeto que representa la peticion del cliente
        dir (str): Nombre del directorio donde esta el archivo
        file (str): Nombre del archivo solicitado
        returns (File): Retorna un archivo CSS o JS
        """
        print("enviando: ", file)
        return send_file("/assets/" + dir + "/" + file)



    global client_socket
    global last_key_press
    global historial_de_vuelos

    #done ----------------------
    #para mandar la tecla presionada a la pagina
    @app.route('/get/key')
    def index(request):
        global last_key_press
        response = {"key":last_key_press}
        print("get/key: ",response)
        last_key_press = ""
        json_data = ujson.dumps(response)
        return json_data, 202, {'Content-Type': 'json'}

    
    #done ----------------
    #se repite constantemente
    vuelos = {}
    @app.route('/update/flights')
    #Ruta para la pagina de la CTRT
    def index(request):
        global historial_de_vuelos
        
        for vuelo in historial_de_vuelos:
            vuelos[vuelo] = {"alertas":{}}
            vuelos[vuelo]["alertas"] = historial_de_vuelos[vuelo]["alertas"]
        json_data = ujson.dumps(vuelos)
        
        print("update flights: ","\n")
        return json_data, 202, {'Content-Type': 'json'}
    # vuelos = {'123':{"alertas":{'alert':1, 'emergency':0}},
    #           '324':{"alertas":{'alert':1, 'emergency':0}}
    # }
    


    #done ------------------
    #solo se usa 1 vez cuando entra a el historial de un vuelo
    #envia los nombres de las variables
    @app.route('/get/names/variables')
    def index(request): 
        json_data = ujson.dumps(nombres_variables)
        #lista con nombres de variables
        print("get names variables", "\n")
        #{"variables":["hora","spo1","spo2"]}
        return json_data, 202, {'Content-Type': 'json'}
    

    #done ----------------
    #solo se usa 1 vez cuando entra a el historial de un vuelo
    #envia el historial de datos de ese vuelo
    @app.route('/get/history/<nro_vuelo>')
    def index(request, nro_vuelo):
        json_data = ujson.dumps(historial_de_vuelos[nro_vuelo])
        print("get history nrovuelo", nro_vuelo)
        print(json_data, "\n")
        return json_data, 202, {'Content-Type': 'json'}
        

    #done ------------------
    #crea tabla de aeropuertos
    @app.route('/get/airports')
    def index(request):
        json_data = ujson.dumps(info_aeropuertos)
        print("get airports", "\n")
        return json_data, 202, {'Content-Type': 'json'}


    #en caso de que se perciba peligro o intentional loss
    @app.route('/send/<nrovuelo>/<instruccion>')
    def index(request, nrovuelo, instruccion):
        print("send to ", nrovuelo, " instruccion: ", instruccion, "\n")
        stationctrt.send_message(client_socket, str(instruccion))            #"aterriza", "no_aterrizes"
        return
    
    #done ------------------------    
    #en caso de solicitud
    @app.route('/send/<nro_vuelo>/info_airport/<indice>')
    def index(request, nro_vuelo, indice):
        aeropuerto = {'info aeropuerto': info_aeropuertos['airports'][int(indice)]}
        print("send to: ", nro_vuelo, " airport: ", aeropuerto, "\n")
        stationctrt.send_message(client_socket, aeropuerto)
        return {"enviado":1}, 202, {'Content-Type': 'json'}
    
    app.run(port=80)


# Inicio la medicion del sensor
print("iniciar keypad")
_thread.start_new_thread(teclas, ())

print("iniciar manage aes")
_thread.start_new_thread(manage_AES, ())

    
print("conectar microdot")
print("Microdot corriendo en IP/Puerto: ",sta_if, ":80")
conectar_microdot()



# Inicio la aplicacion

