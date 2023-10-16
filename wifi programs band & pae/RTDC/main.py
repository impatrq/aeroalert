import stationrtdcv2 as stationrtdc
from machine import Pin
import time
client_socket = stationrtdc.do_connect()
tipo = "soy_rtdc"
stationrtdc.send_type(client_socket, tipo)




#msg = "aterriza"    # o "no_aterrizes"
#stationrtdc.send_message(client_socket,msg)
pin_luz_roja = Pin(12, Pin.OUT)
pin_luz_ambar = Pin(13, Pin.OUT)
emergency = alert = 0


def alarmas_sonoras ():
    global pin_luz_ambar, pin_luz_roja
    global emergency, alert
    while True:
        time.sleep(2)
        if emergency == 1:
            sound()
        elif alert == 1:
            sound()


def notification(cual):
    global pin_luz_ambar, pin_luz_roja
    global emergency, alert
    if cual == "emergency":
        print("emergency")
        pin_luz_roja.value(1)
        pin_luz_ambar.value(0)
        emergency = 1
        alert = 0

    elif cual == "alert":
        print("alert")
        pin_luz_roja.value(0)
        pin_luz_ambar.value(1)
        alert = 1
        emergency = 0

    elif cual == "clean":
        pin_luz_ambar.value(0)
        pin_luz_roja.value(0)
        alert = 0
        emergency = 0

while True:
    data = stationrtdc.receive_data(client_socket)
    print(data)
    if data == "solicito aterrizaje":
        print("a")
    elif data == "alerta desactivacion del sae":
        print("b")
    elif data == "Sae activado":
        print("c")

    elif type(data) == list:
        info={"bpm_altos1": data[0],         "bpm_altos2": data[1], 
              "bpm_bajos1": data[2],         "bpm_bajos2": data[3], 
                "dormido1": data[4],           "dormido2": data[5],
              "spo_bajos1": data[6],         "spo_bajos2": data[7], 
              "temp_alta1": data[8],         "temp_alta2": data[9], 
              "temp_baja1": data[10],        "temp_baja2": data[11],
                 "muerte1": data[12],           "muerte2": data[13], 
                  "manual": data[14], "pulsera_conectada": data[15],
             "no_reaccion": data[16],        "pin_on_off": data[16]}
        
        if data["no_reaccion"] or data["manual"] or info["muerte1"] and info["muerte2"]:
            notification("emergency")
        else:
            if data["muerte1"] or data["muerte2"]:
                notification("alert")
            elif data["spo_bajos1"] or data["spo_bajos2"]:
                notification("alert")
            elif data["dormido1"] or data["dormido2"]:
                notification("alert")            
            elif not data["pulsera_conectada"] or data["pin_on_off"]:
                notification("alert") 
    if sum(data) == 1:
        notification("clean")
