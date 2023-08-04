import serial
from time import sleep

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=0
    )

print("connected to: " + ser.portstr)


while True:

    leer = ser.read(1)
    read = leer.decode('utf-8')
    if read:
        print(read)

ser.close()
