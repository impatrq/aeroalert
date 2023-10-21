import stationrtdcv2 as stationrtdc
from machine import Pin
from time import sleep
import time
hora = time.localtime()



global client_socket, sta_if
client_socket, sta_if = stationrtdc.do_connect()
stationrtdc.send_type(client_socket, "soy_rtdc")


pin_luz_roja = Pin(12, Pin.OUT)
pin_luz_ambar = Pin(13, Pin.OUT)



# Defininicón de Pines keypad
filas = [16, 4, 0, 2]
columnas = [19, 18, 5, 17]
# Definimos los pines de las filas como salida
pines_Filas = [Pin(pin_nombre, mode=Pin.OUT) for pin_nombre in filas]
# Definimos los pines de las columnas de salida
pines_Columnas = [Pin(pin_nombre, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_nombre in columnas]



alert = emergency = solicitud = sae_desactivado = 0

#informacion de aeropuertos
info_aeropuertos = [{"aeropuerto":"ezeiza", "coordenadas": [23,43]},
                    {"aeropuerto":"aeroparque", "coordenadas": [54,22]}]

nombres_variables = {"variables":["Hora","bpm_altos1","bpm_altos2","bpm_bajos1","bpm_bajos2","dormido1","dormido2","spo_bajos1","spo_bajos2","temp_alta1","temp_alta2","temp_baja1","temp_baja2","muerte1","muerte2","manual","pulsera_conectada","no_reaccion", "pin_off"]}
historial_de_vuelos = {}


def notification(cual, nro_vuelo, data):
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
    hora_string = str(f"{hora[3]}:{hora[4]}:{hora[5]}")

    info_hora = [hora_string]
    for i in data:  
        info_hora.append(i)
    #info_hora = ["23:23:43",0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]



    alerts = {"alert": alert, "emergency": emergency, "solicitud": solicitud, "sae_desactivado": sae_desactivado}


    if vuelo_nro in historial_de_vuelos:
        historial_de_vuelos[vuelo_nro]["datos con hora"].append(info_hora)
        historial_de_vuelos[vuelo_nro]["alertas"] = alerts
    else:
        historial_de_vuelos[vuelo_nro] = {"datos con hora":[info_hora],"alertas":alerts}

        #historial_de_vuelos = 
        #{'12323': {'datos con hora': [
        #                              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
        #                              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        #                              ], 
        #           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}}



def manage_AES():
    global solicitud, sae_desactivado
    while True:
        recibido = stationrtdc.receive_data(client_socket)
        print("recibido sae: ", recibido)

        msg = recibido("msg")                   #puede ser ""
        nro_vuelo = recibido("nro_vuelo")
        data = recibido("list")                         #recibido = {"msg":"solicito: aterrizaje", "nro_vuelo": 4334, "list": (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)}

        if msg == "solicito aterrizaje":
            solicitud = 1        
        elif msg == "alerta desactivacion del sae":
            sae_desactivado = 1
        elif msg == "Sae activado":
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
        
        if I["no_reaccion"] or I["manual"] or I["muerte1"] and I["muerte2"]:
            notification("emergency",nro_vuelo, data)
        
        elif I["muerte1"] or I["muerte2"] or I["spo_bajos1"] or I["spo_bajos2"] or I["dormido1"] or I["dormido2"] or not I["pulsera_conectada"] or I["pin_on_off"]:
                notification("alert",nro_vuelo,  data)


        elif sae_desactivado == 1:
            notification("alert",nro_vuelo, data)
        if sum(data) == 1 and I["pulsera_conectada"] == 1:
            notification("clean",nro_vuelo, data)




#Función para inicializar el teclado
def inicio():
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
    
    #       * # A B C D
    # enter, arriba, abajo, deseleccionar
    #softreset()

    global last_key_press
    last_key_press = ""
    while True:
        for fila in range(4):
            for columna in range(4):
                tecla = escanear(fila, columna)
                if tecla == Tecla_Abajo:
                    print("Es el numero: ", teclas[fila][columna])
                    last_key_press = teclas[fila][columna]
                    sleep(0.5)
                    last_key_press = ""



from microdot_asyncio import Microdot, send_file
import ujson
import _thread

def conectar_microdot():
    app = Microdot()

    @app.route('/')
    def index(request):
        return send_file("index.html")

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
        return send_file("/assets/" + dir + "/" + file)



    global client_socket
    global last_key_press
    global historial_de_vuelos

    #done ----------------------
    #para mandar las teclas presionadas a la pagina
    @app.route('/update/keys')
    def index(request):
        print("Key to page")
        response = {"key":last_key_press}
        json_data = ujson.dumps(response)
        return json_data, 202, {'Content-Type': 'json'}

    #done ----------------
    #se repite constantemente mientras esta en el inicio
    vuelos = {}
    @app.route('/update/flights')
    def index(request):
        for vuelo in historial_de_vuelos:
            vuelos[vuelo] = {"alertas":{}}
            vuelos[vuelo]["alertas"] = historial_de_vuelos[vuelo]["alertas"]
        json_data = ujson.dumps(vuelos)
        print("update flights")
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
        print("get names variables")
        #{"variables":["hora","spo1","spo2"]}
        return json_data, 202, {'Content-Type': 'json'}
    

    #done ----------------
    #solo se usa 1 vez cuando entra a el historial de un vuelo
    #envia el historial de datos
    @app.route('/get/history/<nro_vuelo>')
    def index(request, nro_vuelo):
        json_data = ujson.dumps(historial_de_vuelos[nro_vuelo])
        print("get histyory nrovuelo")
        return json_data, 202, {'Content-Type': 'json'}
        

    #done ------------------
    #si ingresa para mandar un aeropuerto
    @app.route('/get/airports')
    def index(request):
        json_data = ujson.dumps(info_aeropuertos)
        print("get airports")
        return json_data, 202, {'Content-Type': 'json'}


    #en caso de que se perciba peligro o intentional loss
    @app.route('/send/<nrovuelo>/<instruccion>')
    def index(request, nrovuelo, instruccion):
        print("send ", nrovuelo, " instruccion")
        stationrtdc.send_message(client_socket, str(instruccion))            #"aterriza", "no_aterrizes"
        return
    
    #done ------------------------    
    #en caso de solicitud
    @app.route('/send/<nro_vuelo>/info_airport/<index>')
    def index(request, nro_vuelo, index):
        aeropuerto = {'info aeropuerto': info_aeropuertos[index]}
        print("send to:", nro_vuelo, "info_aeropuerto:",index)
        stationrtdc.send_message(client_socket, aeropuerto)
        return

    
    app.run(port=80)


if __name__ == "__main__":
    try:
        # Inicio la medicion del sensor        
        _thread.start_new_thread(teclas, ())


        conectar_microdot()
        print("Microdot corriendo en IP/Puerto: " + sta_if + ":80")
        

        # Inicio la aplicacion
        
    
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")


