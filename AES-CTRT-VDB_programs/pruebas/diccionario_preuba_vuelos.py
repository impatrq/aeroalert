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

    info = [hora_string,  alert , emergency , solicitud , sae_desactivado ]

    
    if nro_vuelo in historial_de_vuelos:
        historial_de_vuelos[str(nro_vuelo)][0][].append(info)
    else:
        historial_de_vuelos[str(nro_vuelo)] = [[   "hora"  , "alert","emergency","solicitud","sae_desactivado"]]
        historial_de_vuelos[str(nro_vuelo)][0][0].append(info)
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



