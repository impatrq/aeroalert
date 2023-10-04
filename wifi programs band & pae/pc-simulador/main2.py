


client_socket = do_connect()
send_type('soy_PC', client_socket)
send_message(client_socket, 'info de copiloto')

while True:
    instruccion = receive_data(client_socket)
    if instruccion == "ATERRIZAR":
        #send al xplane
        print("aterrizar")
    elif instruccion== "NO ATERRIZAR":
        #send al xplane
        print("no aterrizar")

