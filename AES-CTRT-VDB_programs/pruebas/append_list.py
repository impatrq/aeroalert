import _thread
import random
import time


r = 0

def cambiar_valor_random(a,b):
    
    time.sleep(1)
    print(r, " valor en thread")
    

_thread.start_new_thread(cambiar_valor_random,(1,20))

def escribir():
    global r
    r = 10
    print("cambiaado en escribir a ", r)
    time.sleep(2)
    print(r,"valor en escribir")

escribir()