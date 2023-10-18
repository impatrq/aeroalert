import serial
from time import sleep

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=0
    )
if not ser.isOpen():
    ser.open()

print("connected to: " + ser.portstr)


while True:

    leer = ser.readline()
    read = leer.decode('utf-8')
    if read:
        print(read)

ser.close()
