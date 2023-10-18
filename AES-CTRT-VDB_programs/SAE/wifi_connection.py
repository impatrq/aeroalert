try:
    import usocket as socket
except:
    import socket
import network
import esp
esp.osdebug(None)
import gc

def connect_wifi():
    gc.collect()

    addr = socket.getaddrinfo('192.168.4.1', 8000)[0][-1]
    ssid = 'ESP32'
    password = 'aeroalert'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    ap.config(authmode=3)
    while not ap.active():
        pass

    print('Connection successful')
    print(ap.ifconfig())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8000))  # or addr
    s.listen(2)
    print("Listening on", addr)

    return s
