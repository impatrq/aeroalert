import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel
from arcade.gui.events import UIOnChangeEvent


class Boton(arcade.gui.UITextureButton):
    def __init__(self, mensa_Al:str, mensa_BA:str):
        super().__init__(
            texture = arcade.load_texture("llave.png"),
            texture_pressed = arcade.load_texture("llave.png")
        )

        self.variable = True

        self.mensajeA = mensa_Al
        self.mensajeB = mensa_BA

        self.on_click = self.button_clicked
        self.scale(0.17)

    def On_button_on(self):
        if self.variable == True:
            self.texture = \
                arcade.load_texture("llave2.png")
            self.variable = False
            print(self.mensajeB)
        elif self.variable == False:
            self.texture = \
                arcade.load_texture("llave.png")
            self.variable = True
            print(self.mensajeA)

    def button_clicked(self, *_):
        self.On_button_on()

class Barrita(UISlider):
    def __init__(self, valor:int, ValorM:int, ValorMin:int, Width:int, Height:int, X:int):
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

        #ui_slider = UISlider(value=self.valor, width=Width, height=50)
        self.label = UILabel(text=f"{self.value:02.0f}")

        @self.event()
        def on_change(event: UIOnChangeEvent):
            self.label.text = f"{self.value:02.0f}"
            self.label.fit_content()
    def Label(self):
        return self.label

        


class MyView(arcade.View):
    def __init__(self, my_window: arcade.Window):
        super().__init__(my_window)

        self.media_player = None
        self.paused = True
        self.cur_song_index = 0


        
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.ui_manager2 = arcade.gui.UIManager(self.window)


        self.manager = UIManager()
        self.manager.enable()

        box = arcade.gui.UIBoxLayout(vertical = False, space_between=30)
        box1 = arcade.gui.UIBoxLayout(vertical = False, space_between= 30)


        normal_texture = arcade.load_texture("llave.png")
        hover_texture = arcade.load_texture("llave.png")
        press_texture = arcade.load_texture("llave.png")





        self.button2 = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_pressed=press_texture,
        )

        self.button2.on_click = self.button2_clicked
        self.button2.scale(0.17)

        box.add(self.button2)


        self.variable = True
        self.variable1 = True
        self.variable2 = True


        self.boton1 = Boton("Pulso Alto 2","Pulso Bajo 2")
        box.add(self.boton1)

        self.boton2 = Boton("Nnormal 2","Muerte 2")
        box.add(self.boton2)

        self.boton3 = Boton("Normal hy 2","Hipoxia 2")
        box.add(self.boton3)
        '''

        self.boton4 = Boton("Normal som 1","Somnolencia 1")
        box1.add(self.boton4)

        self.boton5 = Boton("Pulso Alto 1","Pulso Bajo 1")
        box1.add(self.boton5)

        self.boton6 = Boton("Nnormal 1","Muerte 1")
        box1.add(self.boton6)

        self.boton7 = Boton("Normal hy 1","Hipoxia 1")
        box1.add(self.boton7)'''

        self.barra1 = Barrita(50, 100, 0, 300, 50,0)
        self.Label1 = self.barra1.Label()

        self.barra2 = Barrita(75, 150, 0, 300, 50,0)
        self.Label2 = self.barra2.Label()


        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box, anchor_y= "top", align_y=-70))
        self.ui_manager2.add(arcade.gui.UIAnchorWidget(child=box1, anchor_y= "bottom", align_y= 20))
        self.manager.add(UIAnchorWidget(child=self.barra1, align_y= -60))
        self.manager.add(UIAnchorWidget(child=self.Label1, align_y=-30))

        self.manager.add(UIAnchorWidget(child=self.barra2, anchor_y="bottom"))
        self.manager.add(UIAnchorWidget(child=self.Label2, align_y=-130))

     
    def button2_on(self):
        if self.variable2 == True:
            self.button2.texture = \
                arcade.load_texture("llave2.png")
            self.variable2 = False
            print("Somnolencia 2")
        elif self.variable2 == False:
            self.button2.texture = \
                arcade.load_texture("llave.png")
            self.variable2 = True
            print("Normal som 2")
            
    
    def button2_clicked(self, *_):
        self.button2_on()


    def on_draw(self):
        self.clear()

        #Arriba
        arcade.draw_text("Hipoxia", 470 , 310, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")
        
        arcade.draw_text("Muerte", 355 , 310, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulso", 240 , 310, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Somnolencia", 130 , 310, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulsaciones", 300 , 80, arcade.color.WHITE, font_size=15, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Saturacion de oxigeno", 300 , 180, arcade.color.WHITE, font_size=15, font_name= "calibri" ,anchor_x="center")


        #Bajo 
        '''
        arcade.draw_text("Hipoxia", 470 , 115, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")
        
        arcade.draw_text("Muerte", 355 , 115, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Pulso", 240 , 115, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")

        arcade.draw_text("Somnolencia", 130 , 115, arcade.color.WHITE, font_size=20, font_name= "calibri" ,anchor_x="center")'''




        arcade.draw_text("Piloto 2", 300 , 340, arcade.color.WHITE, font_size=26, font_name= "calibri" ,anchor_x="center")

        #arcade.draw_text("Piloto 1", 300 , 145, arcade.color.WHITE, font_size=26, font_name= "calibri" ,anchor_x="center")

        self.ui_manager.draw()
        self.manager.draw()
        self.ui_manager2.draw()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)

        self.ui_manager.enable()
        self.ui_manager2.enable()

    def on_hide_view(self):
        self.ui_manager.disable()
        self.ui_manager2.disable()


if __name__ == "__main__":
    window = arcade.Window(width = 600, height=370, title="A")
    window.show_view(MyView(window))
    arcade.run()