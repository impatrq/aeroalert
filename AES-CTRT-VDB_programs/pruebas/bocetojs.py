index = 1
index_flights = 1
index_data = 1


#la lista que recibe del micro
max_airports = len(airports)
max_vuelos = len(vuelos)
max_data = len(max_vuelos[data_con_hora])

def cambiar_interfaz(a_cual, index):
    if a_cual == "flights":
        cambiar_vuelo_seleccionado(index)

    elif a_cual == "flight":
        b

    elif a_cual == "airports":
        c




if interfaz == "flights":
        
    if inpt == "2":         #flecha para arriba
        if index_flights != 1:
            index_flights = index_flights -1
            cambiar_vuelo_seleccionado(index_flights)

    elif inpt == "8":       #flecha para abajo
        if index_flights != max_vuelos:
            index_flights = index_flights+1
            cambiar_vuelo_seleccionado(index_flights)

    if inpt == "6":         #enter o derecha 
        cambiar_interfaz("flight", index_flights)
        interfaz = "flight"
        


elif interfaz == "flight":
    
    if inpt == "2":         #flecha para arriba
        if index_data > 1:
            index_data = index_data -1
            cambiar_data_seleccionada(index_data)

    elif inpt == "8":       #flecha para abajo
        if index_data < max_data:
            index_data = index_data+1
            cambiar_data_seleccionada(index_data)


    if inpt == "4":  #para atras o izquierda
        cambiar_interfaz("flights", index_flights)
        interfaz = "flights"
        index_data = 1
    if inpt == "6":         #enter o derecha 
        cambiar_interfaz("airports", index)
        index_data = 1


    if inpt == "A":
        enviar_instruccion("aterriza",index_flights)
    elif inpt == "B":
        enviar_instruccion("no aterrizes",index_flights)


elif interfaz == "airports":
    if inpt == type(int):   #cualquier numero para seleccionar airport
        if inpt <= max_airport:
            enviar_airport(inpt)
            cambiar_interfaz("flights", index_flights)
            interfaz = "flights"

    if inpt == "A":
        enviar_instruccion("aterriza",index_flights)
    elif inpt == "B":
        enviar_instruccion("no aterrizes",index_flights)

    if inpt == "C":         #para cancelar
        cambiar_interfaz("flight", index_flights)
        interfaz = "flight"            






if inpt == "D":
    refreshPage()