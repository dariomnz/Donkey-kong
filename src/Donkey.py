import pyxel
from Sprite import Sprite
class Donkey(Sprite):
    """Clase del mono"""
    def __init__(self,x:int,y:int):
        """Cronstructor del mono"""

        ### Tamaño y ubicacion de las imagenes ###
        self.width_image_map=( 38 ,)
        self.height_image_map=(32 ,)
        self.x_image_map=(     0  ,)
        self.y_image_map=(     215,)

        ### Variables para la animacion ###
        self.animation={
        'IDLE1':0,'IDLE2':1,
        }
        self.current_animation='IDLE1'

        ### Constructor del padre ###
        Sprite.__init__(self,x,y,
        self.x_image_map,
        self.y_image_map,
        self.width_image_map,
        self.height_image_map,
        1)


    def update(self):
        ### Contador de la imagen de la animacion ###
        self.counter=self.get_counter_animation()


    def get_counter_animation(self)->int:
        return self.animation.get(self.current_animation)