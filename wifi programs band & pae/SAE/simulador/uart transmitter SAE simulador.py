from machine import UART
from time import sleep
uart = UART(1, 115200) # 1st argument: UART number: Hardware UART #1


while True:
# Write
    uart.write("1")
    print("1")
    sleep(1)
    
    
# Read
#print(uart.read()) # Read as much as possible using


