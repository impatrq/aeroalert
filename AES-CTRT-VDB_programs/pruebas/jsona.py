
import json
aeropuertos = {"airports":[ {"nombre": "Ezeiza", "coordenadas": ["34°49′25″, 58°31′44″"]},
                {"nombre": "Aeroparque", "coordenadas": ["34°33'27″ 58°24'43″"]},
                {"nombre": "Ambrosio Taravella", "coordenadas": ["31°19'03″ 64°12'36″"]},
                {"nombre": "Moron", "coordenadas": ["33°29'13″ 54°52'26″"]},
                {"nombre": "Quilmes", "coordenadas": ["35°34'17″ 57°54'45″"]}]}


json_data = json.dumps(aeropuertos)
#print(json_data)
#print(json_data, 202, {'Content-Type': 'json'})
historial_vuelos= {
                    "12323":{
                            'datos con hora':[
                                              [1,2,3],[123,23,34,4],
                                              [123,23,34,4],[123,23,34,4],
                                              [123,23,34,4],[123,23,34,4],
                                              [123,23,34,4],[123,23,34,4],
                                              [123,23,34,4],[123,23,34,4],
                                              [1,2,3,344,4],[123,23,34,4],
                                              [123,2655656456456456],[123,23,34,4],
                                              [123,23,34,4],[123,23,34,4],
                                              [123,23,34,4],[123,23,34,4],
                                              [123,23,34,4],[3,2,1]
                                             ],
                            'alertas':{'alert':1, 'emergency':0,
                                       'solicitud':0, 'sae_desactivado':1}
                            },

                    "122324324":{
                                'datos con hora':[
                                              [1,2,3,344,4],
                                              [123,23,34,4]
                                             ],
                                'alertas':{'alert':1, 'emergency':0,
                                       'solicitud':0, 'sae_desactivado':1}
                            }
                    }

historial_vuelos['12323']['datos con hora'] = historial_vuelos['12323']['datos con hora'][-19:]
print(historial_vuelos['12323']['datos con hora'])
#historial_vuelos['12323']["datos con hora"] = historial_vuelos['12323']["datos con hora"][-20:]
#print(historial_vuelos['12323'])
#
#vuelos = {}
#for vuelo in historial_vuelos:
#    vuelos[vuelo] = historial_vuelos[vuelo]['alertas']
#
#print(vuelos)