import serial
from playsound import playsound
import time
import xplane
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=0
    )
print("connected to: " + ser.portstr)
prendida1 = prendida2 = 0
while True:
    leer = ser.readline()
    read = leer.decode('utf-8')
    if read:
        print(read)
        if read == "apagar alarma_sonora_1":
            prendida1 = 0
        elif read == "prender alarma_sonora_1" or prendida1:
            playsound("alarma_1.mp3")
            prendida1 = 1
            time.sleep(2)
        elif read == "apagar alarma_sonora_2":
            prendida2 = 0
        elif read == "prender alarma_sonora_2" or prendida2:
            playsound("alarma_2.mp3")
            prendida2 = 1
            time.sleep(2)
        elif read == "aterrizar":
            xplane.send(1)
        elif read == "no aterrizar":
            xplane.send(0)
            
