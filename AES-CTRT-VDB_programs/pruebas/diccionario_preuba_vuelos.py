import time

nombres_variables = ["Hora","bpm_altos1","bpm_altos2","bpm_bajos1","bpm_bajos2","dormido1","dormido2","spo_bajos1","spo_bajos2","temp_alta1","temp_alta2","temp_baja1","temp_baja2","muerte1","muerte2","manual","pulsera_conectada","no_reaccion", "pin_off"]
historial_de_vuelos = {}


for i in range(2):
    
    alert = 1
    emergency = 0
    solicitud = 1
    sae_desactivado = 0


    data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)
    nro_vuelo = 12323

    vuelo_nro = str(nro_vuelo)

    hora = time.localtime()
    hora_string = str(f"{hora[3]}:{hora[4]}:{hora[5]}")

    info_hora = [hora_string]
    for i in data:  
        info_hora.append(i)
    #info_hora = ["23:23:43",0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]



    alerts = {"alert": alert, "emergency": emergency, "solicitud": solicitud, "sae_desactivado": sae_desactivado}


    if vuelo_nro in historial_de_vuelos:
        historial_de_vuelos[vuelo_nro]["datos con hora"].append(info_hora)
        historial_de_vuelos[vuelo_nro]["alertas"] = alerts
    else:
        historial_de_vuelos[vuelo_nro] = {"variables":nombres_variables, "datos con hora":[info_hora],"alertas":alerts}



        #historial_de_vuelos = 
        #{'12323': {'datos con hora': [
        #                              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
        #                              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        #                              ], 
        #           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}}

    time.sleep(1)
print(historial_de_vuelos)




