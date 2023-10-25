import serial
from playsound import playsound
import time
#import xplane
import _thread

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=0
    )
print("connected to: " + ser.portstr)



global alarma_sonora_hypoxia, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_manual_activation

alarma_sonora_hypoxia = alarma_sonora_aes_alert = alarma_sonora_sleep = alarma_sonora_manual_activation = 0

def thread_sonidos():
    global alarma_sonora_hypoxia, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_manual_activation
    while True:
        if alarma_sonora_hypoxia:
            playsound()
        if alarma_sonora_aes_alert:
            playsound()
        if alarma_sonora_sleep:
            playsound()
        if alarma_sonora_manual_activation:
            playsound()

_thread.start_new_thread(thread_sonidos, ())

while True:
    leer = ser.readline()
    read = leer.decode('utf-8')
    if read:
        print(read)
        
        if read == "aterrizar":
            xplane.instruccion("aterrizar")
        elif read == "no aterrizar":
            xplane.instruccion("no aterrizar")
        elif type(read) == list:
            if read[0] == "info aeropuerto:":
                xplane.instruccion(read[1])

        elif read == "alarma_sonora_hypoxia = 1":
            alarma_sonora_hypoxia = 1
        elif read == "alarma_sonora_hypoxia = 0"   :
            alarma_sonora_hypoxia = 0

        elif read == "alarma_sonora_aes_alert = 1":
            alarma_sonora_aes_alert = 1
        elif read == "alarma_sonora_aes_alert = 0"    :
            alarma_sonora_aes_alert = 0
        
        elif read == "alarma_sonora_sleep = 1":
            alarma_sonora_sleep = 1
        elif read == "alarma_sonora_sleep = 0"     :
            alarma_sonora_sleep = 0
        
        elif read == "alarma_sonora_manual_activation = 1":
            alarma_sonora_manual_activation = 1
        elif read == "alarma_sonora_manual_activation = 0":
            alarma_sonora_manual_activation = 0
            
