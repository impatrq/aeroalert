#from winsound import PlaySound
from playsound import playsound
import time
import _thread

def th_func(delay, id):
    print("hola",delay,id)
    playsound("C:/Users/manuc/Desktop/github/proyecto/AES-CTRT-VDB_programs/pruebas/sonido-emergency.mp3")
print("awa")
i = 1
_thread.start_new_thread(th_func, (i + 1, i))
print("owo")