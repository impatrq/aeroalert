import time

historial_de_vuelos = {}

nro_vuelo = 12323

for i in range(4):
    hora = time.localtime()
    hora_string = str(f"{hora[3]}:{hora[4]}:{hora[5]}")
    alert = 1
    emergency = 0
    solicitud = 1
    sae_desactivado = 0

    data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)
    
    info_hora = [hora_string]
    for i in data:  
        info_hora.append(data)

    variables = ["Hora","bpm_altos1","bpm_altos2","bpm_bajos1","bpm_bajos2","dormido1","dormido2","spo_bajos1","spo_bajos2","temp_alta1","temp_alta2","temp_baja1","temp_baja2","muerte1","muerte2","manual","pulsera_conectada","no_reaccion", "pin_off"]

    if str(nro_vuelo) in historial_de_vuelos:
        historial_de_vuelos[str(nro_vuelo)]["variables"].append(data)
    else:
        historial_de_vuelos[str(nro_vuelo)] = {"variables":[variables, data]}

        historial_de_vuelos[str(nro_vuelo)] = {"variables":[["hora","bpm_altos1","bpm_altos2","bpm_bajos1","bpm_bajos2","dormido1","dormido2","spo_bajos1","spo_bajos2","temp_alta1","temp_alta2","temp_baja1","temp_baja2","muerte1","muerte2","manual","pulsera_conectada","no_reaccion", "pin_off"],
                                                            [hora_string,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                                                            ],
                                               "alertas":{"alert": alert, "emergency": emergency, "solicitud": solicitud, "sae_desactivado": sae_desactivado}}
        
        historial_de_vuelos[str(nro_vuelo)]["variables"].append(variables)
    time.sleep(1)
print(historial_de_vuelos)

"""historial_de_vuelos= {nro_vuelo:[[   "hora"  , "alert","emergency","solicitud","sae_desactivado"],
                                 [hora_string,  alert , emergency , solicitud , sae_desactivado ],
                                 [],
                                 [],
                                 []],
                            123:[[   "hora"  , "alert","emergency","solicitud","sae_desactivado"],
                                 [hora_string,  alert , emergency , solicitud , sae_desactivado ],
                                 [],
                                 [],
                                 []]         
                                    }
"""



