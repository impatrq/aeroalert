from machine import Timer
import time
pasaron_30segs_spo = pasaron_30segs_bpm = 0
contador_iniciado_60_bpm = contador_iniciado_60_spo = 0
contador_iniciado_30_bpm = contador_iniciado_30_spo = 0
tomar_control = alarmas_off_spo = alarmas_off_bpm = 0
            
t30spo = Timer(0)
t60spo = Timer(0)
t30bpm = Timer(0)
t60bpm = Timer(0)

#despues de que pase el tiempo del timer se va a hacer la accion segun el arg ("cual")
def contador60spo(self):
    global alarmas_off_bpm
    global alarmas_off_spo

    global contador_iniciado_60_spo
    contador_iniciado_60_spo = 0
    alarmas_off_spo = 0
def contador30spo(self):
    global alarmas_off_bpm
    global alarmas_off_spo
    global pasaron_30segs_spo
    pasaron_30segs_spo = 1
    alarmas_off_spo = 0
    
def contador30bpm(self):
    global alarmas_off_bpm
    global alarmas_off_spo
    global pasaron_30segs_bpm
    pasaron_30segs_bpm = 1
    alarmas_off_bpm = 0
    
def contador60bpm(self): 
    global alarmas_off_bpm
    global alarmas_off_spo    
    global contador_iniciado_60_bpm
    contador_iniciado_60_bpm = 0
    alarmas_off_bpm = 0
        


print("programa")
time.sleep(2)
print("timer iniciado")
t30spo.init(mode=Timer.ONE_SHOT, period=3000, callback=contador30spo)

while True:
    print("owo")
    time.sleep(4)