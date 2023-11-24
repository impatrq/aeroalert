#Se activa el sistema al resetear el micro con la excepción de "parado"
try:
    import AES.accesssv9 as accesssv9
except KeyboardInterrupt:
    print("parado")