import machine
import time

luz_ambar = machine.Pin(17, machine.Pin.OUT)             
luz_roja = machine.Pin(4, machine.Pin.OUT)              
luz_test = machine.Pin(14, machine.Pin.OUT)                      
activacion_manual = machine.Pin(21, machine.Pin.IN)
test = machine.ADC(machine.Pin(35))
test.atten(machine.ADC.ATTN_6DB)
reaccion = machine.Pin(19, machine.Pin.IN)            
on_off = machine.Pin(18, machine.Pin.IN)  #reemplazar por test el num
flag = machine.Pin(26, machine.Pin.OUT)

while True:
    print(luz_ambar.value(), luz_roja.value(), luz_test.value(),
          activacion_manual.value(),0, reaccion.value(),
          on_off.value(), flag.value(), )
    print(test.read_uv())
    print()
    time.sleep(0.3)
# ambar, roja, test,    manual,    test, reaccion,     off,        flag