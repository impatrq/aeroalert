import machine
import time

g23 = machine.Pin(23, machine.Pin.OUT)            # 
g5 = machine.Pin(5, machine.Pin.OUT)              # 
g17 = machine.Pin(17, machine.Pin.OUT)            # 
g4 = machine.Pin(4, machine.Pin.OUT)              # 
g25 = machine.Pin(25, machine.Pin.OUT)            #
g33 = machine.Pin(33, machine.Pin.OUT)            #       
g35 = machine.Pin(35, machine.Pin.IN)             # LLAVE ON 
                
while True:
    g23.value(0) 
    g5.value(0)  
    g17.value(0) 
    g4.value(0)  
    g25.value(0) 
    g33.value(0)
    g35.value(0)
    print("en 0 todos")
    time.sleep(2)

    g23.value(1)
    g5.value(1)
    g17.value(1)
    g4.value(1)
    g25.value(1)
    g33.value(1)
    print(g35.value())
    print("en 1 todos")
    time.sleep(2)
