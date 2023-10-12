def uartsito():
    from machine import UART
    import time
    a = 1
    uart = UART(1, 9600)                         # init with given baudrate
    uart.init(9600, bits=8, parity=None, stop=1)
    while True:
        time.sleep(1)
        a = a+1
        print("awa")
        if a >= 20:
            print("terminado")
            break
uartsito()