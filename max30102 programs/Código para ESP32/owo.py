

import Timer
from time import sleep

oledC = Pulso()
#crea el objeto de clase pulso
oledC.muestra()
#hace las mediciones
temporiza = Timer(0)
def desborde (Timer):
    print("hola")

#__________________________________________________________________
temporiza.init(period=1000,mode=Timer.PERIODIC,callback=desborde)
#_________________________________________________________________

while(1):
    print("chau")
    sleep(1)

