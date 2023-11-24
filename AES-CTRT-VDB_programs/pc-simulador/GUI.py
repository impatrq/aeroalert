import arcade, arcade.gui
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel
from arcade.gui.events import UIOnChangeEvent
#pip install arcade     y   pip install wireless

import stationPCv1 as station
import threading, json, time

def wifi():
    global client_socket
    print("intentando conectar")
    client_socket = station.do_connect()
    station.send_type("soy_PC", client_socket)
    print("tipo enviado")

thread = threading.Thread(target=wifi, args=())  
# Inicia un proceso en paralelo para enviar informacion al SAE
thread.start()                                   


"""    while True:
        data = station.receive_data(client_socket)
        instruccion = json.loads(data.decode('utf-8'))

        if instruccion == "ATERRIZAR":     
            print("aterrizar")              # mandar al xplane
        elif instruccion== "NO ATERRIZAR":
            print("no aterrizar")           # mandar al xplane
        time.sleep(1)
"""


global Dicc 

#creamos la clase boton 
class Boton(arcade.gui.UITextureButton):
    def __init__(self, mensa_Al:str, mensa_BA:str):
        super().__init__(
            # definimos las imagenes a utilizar
           texture = arcade.load_texture("imagenes_GUI/llave.png"),
           texture_pressed=arcade.load_texture("imagenes_GUI/llave.png"))
        self.variable = True

        self.mensajeA = mensa_Al
        self.mensajeB = mensa_BA
        self.mensaje = self.mensajeA

        self.on_click = self.button_clicked
        self.scale(0.23) #0.17

    #creamos la funcion On_button_on para el cambio de imagen al presionar sobre el boton
    def On_button_on(self):
        if self.variable == True:
            self.texture = \
                arcade.load_texture("imagenes_GUI/llave2.png")
            self.variable = False
            self.mensaje = self.mensajeB
        elif self.variable == False:
            self.texture = \
                arcade.load_texture("imagenes_GUI/llave.png")
            self.variable = True
            self.mensaje = self.mensajeA

    def valor_boton (self):
        return self.mensaje

    def button_clicked(self, *_):
        self.On_button_on()

#creamos la clase barra
class Barra(UISlider):
    def __init__(self, valor:int, ValorM:int, 
                 ValorMin:int, Width:int, Height:int, X:int):
        super().__init__(
            valor = valor, 
            width = Width, 
            height = Height,
            max_value= ValorM,
            min_value= ValorMin,
            size_hint_min=X
        )
        self.manager = UIManager()
        self.manager.enable()

        self.a = int(0)
        self.label = UILabel(text=f"{self.value:02.0f}")

        @self.event()
        def on_change(event: UIOnChangeEvent):
            self.label.text = f"{self.value:02.0f}"
            self.a = self.value
            self.label.fit_content()
            self.valor()
            
    def Label(self):
        return self.label
    
    def valor(self):
        return self.a

#creamos la clase diccionario para el armado de los datos a enviar 
class Diccionario():
    def __init__(self, Piloto:"0", Hipoxia:"0", Muerte:"0", 
        Somnolencia:"0",Pulso2:"0", Pulso:int, Saturacion:int
        ):
        super().__init__()
        self.Piloto_valor = Piloto
        self.Hipoxia_valor = Hipoxia 
        self.Muerte_valor = Muerte
        self.Somnolencia_valor = Somnolencia
        self.Pulso_valor = int(Pulso)
        self.Pulso_estado = Pulso2
        self.Saturacion_valor = int(Saturacion)
        self.Dic = {
            'Piloto' : self.Piloto_valor,
            'Muerte' : self.Muerte_valor,
            'Hipoxia' : self.Hipoxia_valor,
            'Somnolencia' : self.Somnolencia_valor,
            'Pulso' : self.Pulso_estado,
            'Bpm' : self.Pulso_valor,
            'Spo2' : self.Saturacion_valor
        }
        self.dicc = self.Dic
        print(self.Dic)
    # la funcion valor para que devuelva el mensaje armado 
    def valor (self):
        return self.dicc


#definimos la clase MyView, que es hija de la clase arcade.View
class MyView(arcade.View):

    # se declaran todos los elemtnos a utilizar 
    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager(self.window)
        self.ui_manager2 = arcade.gui.UIManager(self.window)
        self.ui_manager3 = arcade.gui.UIManager(self.window)

        self.manager = UIManager()
        self.manager.enable()

        box = arcade.gui.UIBoxLayout(vertical = False, space_between=70)
        box2 = arcade.gui.UIBoxLayout(vertical = True, space_between= 45)


        normal_texture1 = arcade.load_texture("imagenes_GUI/boton2.png")

        self.button3 = arcade.gui.UITextureButton(
            texture=normal_texture1
        )

        self.button3.on_click = self.button3_clicked
        self.button3.scale(1.08)

        box2.add(self.button3)

        ########################

        self.button4 = arcade.gui.UITextureButton(
            texture=normal_texture1
        )

        self.button4.on_click = self.button4_clicked
        self.button4.scale(1.08)

        box2.add(self.button4)

        ########################


        self.variable = True
        self.variable1 = True
        self.variable2 = True
        self.variable3 = True
        self.variable4 = True


        # se crean los botones a utilizar, com los mensajes a enviar en cada caso 
        self.boton1 = Boton("0","1")          #pulsaciones
        self.boton1.on_click = self.boton_clicked1
        box.add(self.boton1)

        self.boton2 = Boton("0","1")          #muerte
        self.boton2.on_click = self.boton_clicked2
        box.add(self.boton2)

        self.boton3 = Boton("0","1")          #hipoxia
        self.boton3.on_click = self.boton_clicked3
        box.add(self.boton3)

        self.boton4 = Boton("0","1")          #somnolencia
        self.boton4.on_click = self.boton_clicked
        box.add(self.boton4)

        self.boton5 = Boton("a","b")
        box2.add(self.boton5)
        self.boton5.on_click = self.boton_clicked4

        #Tambien se crean las barras 
        self.barra1 = Barra(50, 100, 0, 300, 70,0)
        self.Label1 = self.barra1.Label()
        
        self.barra2 = Barra(75, 150, 0, 300, 70,0)
        self.Label2 = self.barra2.Label()

                
        #se establecen los layout para los botones, como para las barras 
        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box, anchor_y= "top", align_y=-170))
        self.ui_manager3.add(arcade.gui.UIAnchorWidget(child=box2, anchor_y= "bottom", align_y= 50, align_x= 250))

        self.manager.add(UIAnchorWidget(child=self.barra1, align_y= -30))
        self.manager.add(UIAnchorWidget(child=self.Label1, align_y = 0))

        self.manager.add(UIAnchorWidget(child=self.barra2, align_y= -160))
        self.manager.add(UIAnchorWidget(child=self.Label2, align_y= -130))



        self.valor1 = int
        self.valor2 = int


    
    def button3_on(self):
        if self.variable3 == True:
            pass
        elif self.variable3 == False:
            #se cmabia la pestaña del programa
            self.window.show_view(MenuView())

            #se crea el mensaje con los datos
            self.Dicc = Diccionario("2", self.boton3.On_button_on(), self.boton2.On_button_on(), self.boton4.On_button_on(), self.boton1.valor_boton(),self.valor2, self.valor1)

    def button4_on(self):
        if self.variable4 == True:
            self.variable4 = False
        elif self.variable4 == False:
            self.variable4 = True

            dic = self.Dicc.Dic
            #se envia el mensaje por wifi 
            station.send_message(client_socket, dic)

    '''Las siguentes funciones deteminan cambios y procedimientos
        cuando son presionados los botones '''
    def button3_clicked(self, *_):
        self.button3_on()
        if self.variable3 == True:
            self.variable3 = False
        elif self.variable3 == False:
            self.variable3 = True
        
    def button4_clicked(self, *_):
        self.button4_on()

    def boton_clicked(self, *_):
        self.boton4.On_button_on()
        self.Dicc = Diccionario("2", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)

    def boton_clicked1(self, *_):
        self.boton1.On_button_on()
        self.Dicc = Diccionario("2", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)

    def boton_clicked2(self, *_):
        self.boton2.On_button_on()
        self.Dicc = Diccionario("2", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)

    def boton_clicked3(self, *_):
        self.boton3.On_button_on()
        self.Dicc = Diccionario("2", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)

    def boton_clicked4(self, *_):
        self.boton5.On_button_on()
        self.Dicc = Diccionario("2", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)
        
        station.send_message(client_socket, "1")        # Envia un 1 para que use la informacion anterior

    def on_draw(self):
        self.clear()
        self.valor1= self.barra1.valor()
        self.valor2 = self.barra2.valor()
        
        # se dibujan en pantalla las palabras

        #Arriba
        arcade.draw_text("Hipoxia", 775 , 620, arcade.color.WHITE, font_size=25, font_name= "calibri" ,anchor_x="center")
        
        arcade.draw_text("Muerte", 590 , 620, arcade.color.WHITE, font_size=25, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulso", 405 , 620, arcade.color.WHITE, font_size=25, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Somnolencia", 960 , 620, arcade.color.WHITE, font_size=22, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulsaciones", 680 , 290, arcade.color.WHITE, font_size=17.5, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Saturacion de oxigeno", 680 , 420, arcade.color.WHITE, font_size=17.5, font_name= "calibri" ,anchor_x="center")


        arcade.draw_text("Enviar", 935 , 300, arcade.color.WHITE, font_size=22, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Siguiente", 935 , 440, arcade.color.WHITE, font_size=21.5, font_name= "calibri" ,anchor_x="center")                                   
        arcade.draw_text("Activación", 935 , 170, arcade.color.WHITE, font_size=21.5, font_name= "calibri" ,anchor_x="center")





        arcade.draw_text("Piloto 2", 670 , 700, arcade.color.WHITE, font_size=29, font_name= "calibri" ,anchor_x="center")


        self.ui_manager.draw()
        self.manager.draw()
        self.ui_manager3.draw()


    def on_show_view(self):
        #se establece el color del fondo 
        arcade.set_background_color(arcade.color.GRAY)

        self.ui_manager.enable()
        self.ui_manager3.enable()

    def on_hide_view(self):
        self.ui_manager.disable()
        self.ui_manager3.disable()
    
#se crea la siguente pestaña para el piloto 2
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.ui_manager2 = arcade.gui.UIManager(self.window)
        self.ui_manager3 = arcade.gui.UIManager(self.window)


        self.manager = UIManager()
        self.manager.enable()

        box = arcade.gui.UIBoxLayout(vertical = False, space_between=70)
        box1 = arcade.gui.UIBoxLayout(vertical = False, space_between= 30)
        box2 = arcade.gui.UIBoxLayout(vertical = True, space_between= 30)

        normal_texture1 = arcade.load_texture("imagenes_GUI/boton2.png")

        self.button3 = arcade.gui.UITextureButton(
            texture=normal_texture1
        )

        self.button3.on_click = self.button3_clicked
        self.button3.scale(1.08)

        box2.add(self.button3)


        self.button4 = arcade.gui.UITextureButton(
            texture=normal_texture1
        )

        self.button4.on_click = self.button4_clicked
        self.button4.scale(1.08)

        box2.add(self.button4)


        self.variable = True
        self.variable1 = True
        self.variable2 = True
        self.variable3 = True
        self.variable4 = True

        self.boton4 = Boton("0","1")          #dormido
        self.boton4.on_click = self.boton_clicked
        box.add(self.boton4)

        self.boton1 = Boton("0","1")          #muerto
        box.add(self.boton1)
        self.boton1.on_click = self.boton_clicked1

        self.boton2 = Boton("0","1")          #pulso 
        box.add(self.boton2)
        self.boton2.on_click = self.boton_clicked2

        self.boton3 = Boton("0","1")          #hipoxia
        box.add(self.boton3)
        self.boton3.on_click = self.boton_clicked3

        self.boton5 = Boton("usar","usar")
        box1.add(self.boton5)
        self.boton5.on_click = self.boton_clicked4
        

        self.barra1 = Barra(50, 100, 0, 300, 70,0)
        self.Label1 = self.barra1.Label()
        
        self.barra2 = Barra(75, 150, 0, 300, 70,0)
        self.Label2 = self.barra2.Label()


        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box, anchor_y= "top", align_y=-170))
        self.ui_manager2.add(arcade.gui.UIAnchorWidget(child=box1, anchor_y= "bottom", align_y= 70, align_x= -250))
        self.ui_manager3.add(arcade.gui.UIAnchorWidget(child=box2, anchor_y= "bottom", align_y= 20, align_x= 250))
        self.manager.add(UIAnchorWidget(child=self.barra1, align_y= -30))
        self.manager.add(UIAnchorWidget(child=self.Label1, align_y = 0))

        self.manager.add(UIAnchorWidget(child=self.barra2, align_y= -160))
        self.manager.add(UIAnchorWidget(child=self.Label2, align_y= -130))


    def button3_on(self):
        if self.variable3 == True:
            pass
        elif self.variable3 == False:
            self.window.show_view(MyView())
            self.Dicc = Diccionario("2", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), 0, 0)

    def button4_on(self):
        if self.variable4 == True:
            self.variable4 = False
        elif self.variable4 == False:
            self.variable4 = True

            dic = self.Dicc.Dic
            station.send_message(client_socket, dic)        # Envia la informacion cuando se toca el boton de abajo a la derecha

    

    def button3_clicked(self, *_):
        self.button3_on()

        if self.variable3 == True:
            self.variable3 = False
        elif self.variable3 == False:
            self.variable3 = True

    def button4_clicked(self, *_):
        self.button4_on()
    
    def boton_clicked(self, *_):
        self.boton4.On_button_on()
        self.Dicc = Diccionario("1", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)
    
    def boton_clicked1(self, *_):
        self.boton1.On_button_on()
        self.Dicc = Diccionario("1", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)

    def boton_clicked2(self, *_):
        self.boton2.On_button_on()
        self.Dicc = Diccionario("1", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)

    def boton_clicked3(self, *_):
        self.boton3.On_button_on()
        self.Dicc = Diccionario("1", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)
    
    def boton_clicked4(self, *_):
        self.boton5.On_button_on()
        self.Dicc = Diccionario("1", self.boton3.valor_boton(), self.boton2.valor_boton(), self.boton4.valor_boton(), self.boton1.valor_boton(), self.valor2, self.valor1)
        
        
        
        station.send_message(client_socket, "1")            # Envia la informacion cuando se toca el boton de abajo a la derecha
        

    def on_draw(self):
        self.clear()
        self.valor1= self.barra1.valor() #Valor de barra1
        self.valor2 = self.barra2.valor() #Valor de la barra2
        #print(f"{self.valor2:02.0f}", f"{self.valor1:02.0f}")

        #Arriba
        arcade.draw_text("Hipoxia", 960 , 620, arcade.color.WHITE, font_size=25, font_name= "calibri" ,anchor_x="center")
        
        arcade.draw_text("Muerte", 775 , 620, arcade.color.WHITE, font_size=25, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulso", 590 , 620, arcade.color.WHITE, font_size=25, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Somnolencia", 405 , 620, arcade.color.WHITE, font_size=22, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulsaciones", 680 , 290, arcade.color.WHITE, font_size=17.5, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Saturacion de oxigeno", 680 , 420, arcade.color.WHITE, font_size=17.5, font_name= "calibri" ,anchor_x="center")


        arcade.draw_text("Enviar", 935 , 110, arcade.color.WHITE, font_size=22, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Siguiente", 935 , 230, arcade.color.WHITE, font_size=21.5, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Activación", 430 , 200, arcade.color.WHITE, font_size=21.5, font_name= "calibri" ,anchor_x="center")


        arcade.draw_text("Piloto 1", 670 , 700, arcade.color.WHITE, font_size=29, font_name= "calibri" ,anchor_x="center")


        self.ui_manager.draw()
        self.manager.draw()
        self.ui_manager2.draw()
        self.ui_manager3.draw()


    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)

        self.ui_manager.enable()
        self.ui_manager2.enable()
        self.ui_manager3.enable()

    def on_hide_view(self):
        self.ui_manager.disable()
        self.ui_manager2.disable()
        self.ui_manager3.disable()


if __name__ == "__main__":

    window = arcade.Window(fullscreen=True, resizable=True, title="A")
    view2 = MenuView()
    window.show_view(MenuView())
    arcade.run()

    
    