import time
hora = time.localtime()
hora_inicio = hora
while True:
    hora = time.localtime()
    if hora != hora_inicio:
        while True:
            hora = time.localtime()
            print(hora[2],"/",hora[1],"/",hora[0]," ", hora[3],":", hora[4],":", hora[5])
            time.sleep(1)
