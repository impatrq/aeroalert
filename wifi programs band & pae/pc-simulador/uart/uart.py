import UART
uart = UART(1, 115200) # 1st argument: UART number: Hardware UART #1

print(uart.read()) 