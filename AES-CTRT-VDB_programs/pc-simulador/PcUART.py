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


global alarma_sonora_aes_activation, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_hypoxia, alarma_sonora_manual_activation, alarma_sonora_test_failed, alarma_sonora_test_pass

alarma_sonora_aes_activation = alarma_sonora_aes_alert = alarma_sonora_sleep = alarma_sonora_hypoxia = alarma_sonora_manual_activation = alarma_sonora_test_failed = alarma_sonora_test_pass = 0

def thread_sonidos():
    global alarma_sonora_aes_activation, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_hypoxia, alarma_sonora_manual_activation, alarma_sonora_test_failed, alarma_sonora_test_pass
    while True:
        if alarma_sonora_aes_activation:
            playsound("./imgs_alerts_GUI/alerta_aes_act.mp3")     
        if alarma_sonora_aes_alert:
            playsound("./imgs_alerts_GUI/alerta_aes_alert.mp3")
        if alarma_sonora_sleep:
            playsound("./imgs_alerts_GUI/alerta_get_up.mp3")
        if alarma_sonora_hypoxia:
            playsound("./imgs_alerts_GUI/alerta_hypoxia.mp3")
        if alarma_sonora_manual_activation:
            playsound("./imgs_alerts_GUI/alerta_manual_act.mp3")
        if alarma_sonora_test_failed:
            playsound("./imgs_alerts_GUI/alerta_test_failed.mp3")
            alarma_sonora_test_failed = 0
        if alarma_sonora_test_pass:
            playsound("./imgs_alerts_GUI/alerta_test_pass.mp3")
            alarma_sonora_test_pass = 0
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

        #----
        if read == "alarma_sonora_aes_activation = 1":
            alarma_sonora_aes_activation = 1
        elif read == "alarma_sonora_aes_activation = 0":
            alarma_sonora_aes_activation = 0
        #----
        elif read == "alarma_sonora_hypoxia = 1":
            alarma_sonora_hypoxia = 1
        elif read == "alarma_sonora_hypoxia = 0"   :
            alarma_sonora_hypoxia = 0
        #----
        elif read == "alarma_sonora_aes_alert = 1":
            alarma_sonora_aes_alert = 1
        elif read == "alarma_sonora_aes_alert = 0":
            alarma_sonora_aes_alert = 0
        #-----
        elif read == "alarma_sonora_sleep = 1":
            alarma_sonora_sleep = 1
        elif read == "alarma_sonora_sleep = 0":
            alarma_sonora_sleep = 0
        #----
        elif read == "alarma_sonora_manual_activation = 1":
            alarma_sonora_manual_activation = 1
        elif read == "alarma_sonora_manual_activation = 0":
            alarma_sonora_manual_activation = 0
        #----
        elif read == "alarma_sonora_test_failed":
            alarma_sonora_test_failed = 1
        #----
        elif read == "alarma_sonora_test_pass":
            alarma_sonora_test_pass = 1
        #----
