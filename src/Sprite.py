from distutils.log import error
import pyxel


class Sprite(object):
    
    def __init__(self,x:int,y:int,x_image_map:tuple,y_image_map:tuple,width_image_map:tuple,height_image_map:tuple,map:int,isTransparent=0):
        self.x_image_map=x_image_map
        self.y_image_map=y_image_map
        self.width_image_map=width_image_map
        self.height_image_map=height_image_map
        self.isTransparent=isTransparent
        self.map=map
        
        self.counter=0
        self.isEnable=True
        self.move(x,y)


    def update(self):
        pass
    
    def draw(self):

        ### Dibuja la imagen ###
        pyxel.blt(self.x, self.y, 1,
        self.x_image_map[self.counter],
        self.y_image_map[self.counter],
        self.width_image_map[self.counter],
        self.height_image_map[self.counter],
        self.isTransparent)


    def move(self,x:int,y:int):
        self.x=x
        self.y=y        

    def collision_box(self):
        pass

    def collision(self,sprite) -> bool:
        aux_collision_box_1=self.collision_box()
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

        
