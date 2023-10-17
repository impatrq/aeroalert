from machine import Pin
from time import sleep

# Constantes
Tecla_Arriba   = const(0)
Tecla_Abajo = const(1)

teclas = [['1', '4', '7', '*'], ['2', '5', '8', '0'], ['3', '6', '9', '#'], ['A', 'B', 'C', 'D']]

# Defininicón de Pines
filas = [16, 4, 0, 2]
columnas = [19, 18, 5, 17]

# Definimos los pines de las filas como salida
pines_Filas = [Pin(pin_nombre, mode=Pin.OUT) for pin_nombre in filas]

# Definimos los pines de las columnas de salida
pines_Columnas = [Pin(pin_nombre, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_nombre in columnas]

#Funciónpara inicializar el teclado

def inicio():
    for fila in range(0,4):
        for col in range(0,4):
            pines_Filas[fila].value(0)

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

print("iniciando .............Presione una tecla: ")

# poner todas las columnas en bajo
inicio()
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
