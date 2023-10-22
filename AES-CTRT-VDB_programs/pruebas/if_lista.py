vuelos = {}
#123:{}
#"alerts":{"alert":0,"emergency":0}
historial_de_vuelos = {'12323': {'datos con hora': [
                              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                              ], 
           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}},
           '12345': {'datos con hora': [
                              ['10:18:34', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                              ['10:18:35', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                              ], 
           'alertas': {'alert': 1, 'emergency': 0, 'solicitud': 1, 'sae_desactivado': 0}}}



for i in historial_de_vuelos:
    vuelos[i] = {"alertas":{}}
    vuelos[i]["alertas"] = historial_de_vuelos[i]["alertas"]

print(vuelos)