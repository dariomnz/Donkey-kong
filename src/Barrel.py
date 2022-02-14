import pyxel
from Sprite import Sprite

class Barrel(Sprite):

    """Clase del mono"""
    def __init__(self,x:int,y:int):
        """Cronstructor del mono"""

        ### Tamaño y ubicacion de las imagenes ###
        self.width_image_map=( 12 ,12 ,12 ,12)
        self.height_image_map=(10 ,10 ,10 ,10)
        self.x_image_map=(     10 ,22 ,34 ,46)
        self.y_image_map=(     198,198,198,198)
        ### Variables para el control del movimiento ###
        self.RIGHT=0
        self.LEFT=0
        self.vel_x=2
        ### Variables para la animacion ###
        self.animation={
        'BARREL1':0,'BARREL2':1,'BARREL3':2,'BARREL4':3
        }
        self.current_animation='BARREL1'

        ### Constructor del padre ###
        Sprite.__init__(self,x,y,
        self.x_image_map,
        self.y_image_map,
        self.width_image_map,
        self.height_image_map,
        1)


    def update(self):
        if self.y>55 and self.y<85:
            self.LEFT=0
            self.RIGHT=1
        elif self.y>85 and self.y<118:
            self.LEFT=1
            self.RIGHT=0
        elif self.y>118 and self.y<150:
            self.LEFT=0
            self.RIGHT=1
        elif self.y>150 and self.y<185:
            self.LEFT=1
            self.RIGHT=0
        elif self.y>185 and self.y<215:
            self.LEFT=0
            self.RIGHT=1
        elif self.y>215 and self.y<244:
            self.LEFT=1
            self.RIGHT=0
        
        ### Contador de la imagen de la animacion ###
        self.counter=self.get_counter_animation()


    def point_collision_box(self):
        ### ((x1,y1),(x2,y2)) ###

        ### (x1,y1)-------- ###
        ### |             | ###
        ### |             | ###
        ### |             | ###
        ### --------(x2,y2) ###
        return ((self.x,self.y-10),(self.x+11,self.y))


    def point_collision(self,sprite) -> bool:
        aux_collision_box_1=self.point_collision_box()
        aux_collision_box_2=sprite.collision_box()

        x1_1=aux_collision_box_1[0][0]
        x2_1=aux_collision_box_1[1][0]
        y1_1=aux_collision_box_1[0][1]
        y2_1=aux_collision_box_1[1][1]
        x1_2=aux_collision_box_2[0][0]
        x2_2=aux_collision_box_2[1][0]
        y1_2=aux_collision_box_2[0][1]
        y2_2=aux_collision_box_2[1][1]

        if x2_1>=x1_2 and x1_1<=x2_2 and y2_1>=y1_2 and y1_1<=y2_2:
            return True
        else:
            return False


    def collision_box(self):
        ### ((x1,y1),(x2,y2)) ###

        ### (x1,y1)-------- ###
        ### |             | ###
        ### |             | ###
        ### |             | ###
        ### --------(x2,y2) ###
        return ((self.x+1,self.y+1),(self.x+11,self.y+9))



    def get_counter_animation(self)->int:
        
        if pyxel.frame_count%5==0:
            if self.RIGHT-self.LEFT>0:
                if self.current_animation=='BARREL1':
                    self.current_animation='BARREL2'
                elif self.current_animation=='BARREL2':
                    self.current_animation='BARREL3'
                elif self.current_animation=='BARREL3':
                    self.current_animation='BARREL4'
                elif self.current_animation=='BARREL4':
                    self.current_animation='BARREL1'
            elif self.RIGHT-self.LEFT<0:
                if self.current_animation=='BARREL1':
                    self.current_animation='BARREL4'
                elif self.current_animation=='BARREL2':
                    self.current_animation='BARREL1'
                elif self.current_animation=='BARREL3':
                    self.current_animation='BARREL2'
                elif self.current_animation=='BARREL4':
                    self.current_animation='BARREL3'

        return self.animation.get(self.current_animation)