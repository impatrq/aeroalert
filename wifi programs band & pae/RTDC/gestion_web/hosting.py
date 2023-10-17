from microdot_asyncio import Microdot, send_file
import random
import ujson
import machine
import dht
import _thread
import time


def conectar(ssid, password):
    import network

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
    return sta_if.ifconfig()[0]
    

def medir_sensor():
    global 
    


    while True:
        try:
            
            print("")
        except:
            print("")
        time.sleep(3)    
    



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


@app.route('/update/teclas')
def index(request):
    global last_key_press
    return last_key_press

@app.route('/update/alerts')
def index(request):
    global 

    datos = {'hum': humidity, 'temp': temperature}     #  , 'aleatorio1': random1, 'aleatorio2': random2}
    json_data = ujson.dumps(datos)
    print("info enviada")
    return json_data, 202, {'Content-Type': 'json'}




if __name__ == "__main__":
    
    try:
        # Me conecto a internet
        ip = conectar("Red Alumnos","")
        # Muestro la direccion de IP
        print("Microdot corriendo en IP/Puerto: " + ip + ":80")
        
        # Inicio la medicion del sensor        
        _thread.start_new_thread(keypad, ())

        # Inicio la aplicacion
        app.run(port=80)
    
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")


