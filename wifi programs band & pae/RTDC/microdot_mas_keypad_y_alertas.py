import stationrtdcv2 as stationrtdc
from machine import Pin
from time import sleep

global client_socket, sta_if
client_socket, sta_if = stationrtdc.do_connect()
stationrtdc.send_type(client_socket, "soy_rtdc")


#msg = "aterriza"    # o "no_aterrizes"
#stationrtdc.send_message(client_socket,msg)
pin_luz_roja = Pin(12, Pin.OUT)
pin_luz_ambar = Pin(13, Pin.OUT)
emergency = alert = 0

# Definimos los pines de las filas como salida
pines_Filas = [Pin(pin_nombre, mode=Pin.OUT) for pin_nombre in filas]

# Definimos los pines de las columnas de salida
pines_Columnas = [Pin(pin_nombre, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_nombre in columnas]



alert = emergency = solicitud = sae_desactivado = 0
vuelos = {}
def notification(cual, nro_vuelo):
    global pin_luz_ambar, pin_luz_roja
    global alert, emergency, solicitud, sae_desactivado
    global alerts

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
                                                        #envia a la web page que se pide una solicitud de aterrizaje y emergencias
    info = {"alert": alert, "emergency": emergency, "solicitud": solicitud, "sae_desactivado": sae_desactivado}
    vuelos[nro_vuelo] = info   #{123:{"alert": alert, "emergency": emergency, "solicitud": solicitud, "sae_desactivado": sae_desactivado}}
    solicitud = 0

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

    
        info={"bpm_altos1": data[0],         "bpm_altos2": data[1], 
            "bpm_bajos1": data[2],         "bpm_bajos2": data[3], 
            "dormido1": data[4],           "dormido2": data[5],
            "spo_bajos1": data[6],         "spo_bajos2": data[7], 
            "temp_alta1": data[8],         "temp_alta2": data[9], 
            "temp_baja1": data[10],        "temp_baja2": data[11],
            "muerte1": data[12],           "muerte2": data[13], 
            "manual": data[14], "pulsera_conectada": data[15],
            "no_reaccion": data[16],        "pin_on_off": data[17]}
        
        if info["no_reaccion"] or info["manual"] or info["muerte1"] and info["muerte2"]:
            notification("emergency",nro_vuelo)
        
        elif info["muerte1"] or info["muerte2"] or info["spo_bajos1"] or info["spo_bajos2"] or info["dormido1"] or info["dormido2"] or not info["pulsera_conectada"] or info["pin_on_off"]:
                notification("alert",nro_vuelo)


        if sae_desactivado == 1:
            notification("alert",nro_vuelo)
        if sum(data) == 1:
            notification("clean",nro_vuelo)




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

    # Defininicón de Pines
    filas = [16, 4, 0, 2]
    columnas = [19, 18, 5, 17]


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



    #en caso de que se perciba peligro o intentional loss
    @app.route('/send/aes/<instruccion>')
    def index(request, instruccion):
        stationrtdc.send_message(client_socket, str(instruccion))            #"aterriza", "no_aterrizes"


    info_aeropuertos = [{"aeropuerto":"ezeiza", "coordenadas": [23,43]},
                    {"aeropuerto":"aeroparque", "coordenadas": [54,22]}]

    #en caso de solicitud
    @app.route('/send/<nrovuelo>/info_aeropuerto/<index>')
    def index(request, nrovuelo, index):
        aeropuerto = {'info aeropuerto': info_aeropuertos[index]}
        
        #enviar al <nrovuelo>
        stationrtdc.send_message(client_socket, aeropuerto)
        return



    @app.route('/get/aeropuertos')
    def index(request):
        return info_aeropuertos
    
    #ambas periodicamente en js
    @app.route('/update/teclas')
    def index(request):
        return last_key_press
    
    @app.route('/update/vuelos')
    def index(request):
        global vuelos
        json_data = ujson.dumps(vuelos)
        print("vuelos enviados")
        return json_data, 202, {'Content-Type': 'json'}




if __name__ == "__main__":
    try:
        # Inicio la medicion del sensor        
        _thread.start_new_thread(keypad, ())

        print("Microdot corriendo en IP/Puerto: " + sta_if + ":80")
        

        # Inicio la aplicacion
        app.run(port=80)
    
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")


