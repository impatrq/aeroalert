import stationrtdcv2 as stationrtdc




client_socket = stationrtdc.do_connect()

tipo = "soy_rtdc"
stationrtdc.send_type(tipo, client_socket)
msg = "aterriza"    # o "no_aterrizes"
stationrtdc.send_message(client_socket,msg)
data = stationrtdc.receive_data(client_socket)
