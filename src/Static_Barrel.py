import pyxel
from Sprite import Sprite

class Static_Barrel(Sprite):

    """Clase del barril estatico"""
    def __init__(self,x:int,y:int):
        """Cronstructor del barril estatico"""

        ### Tamaño y ubicacion de las imagenes ###
        self.width_image_map=( 10 ,)
        self.height_image_map=(16 ,)
        self.x_image_map=(     0 ,)
        self.y_image_map=(     198,)

        ### Constructor del padre ###
        Sprite.__init__(self,x,y,
        self.x_image_map,
        self.y_image_map,
        self.width_image_map,
        self.height_image_map,
        1)