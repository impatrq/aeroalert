import arcade
from stationPCv1 import *
import threading, time
client_socket = 1

def wifi():
    global client_socket
    print("intentando conectar")
    client_socket = do_connect()
    print("conectado")
    while True:
        time.sleep(3)
        print("owo")
        instruccion = receive_data(client_socket)
        if instruccion == "ATERRIZAR":
            #send al xplane
            print("aterrizar")
        elif instruccion== "NO ATERRIZAR":
            #send al xplane
            print("no aterrizar")

x = threading.Thread(target=wifi, args=())
print("uwu")
x.start()
print("uwu")

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Happy Face Example"
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

arcade.set_background_color(arcade.color.WHITE)

# Clear screen and start render process
arcade.start_render()

x = 300
y = 300
radius = 200
arcade.draw_circle_filled(x, y, radius, arcade.color.YELLOW)
x = 370
y = 350
radius = 20
arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)
x = 230
y = 350
radius = 20
arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)
x = 300
y = 280
width = 120
height = 100
start_angle = 190
end_angle = 350
arcade.draw_arc_outline(x, y, width, height, arcade.color.BLACK,
                        start_angle, end_angle, 10)
# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()