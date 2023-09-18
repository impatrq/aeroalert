# This is your main script.
from machine import UART
import time
owo = UART(1, 115200)
while True:
    time.sleep(1)
    
    UART.write(owo, "funciono anashe")
    