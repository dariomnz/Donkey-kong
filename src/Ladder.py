import  pyxel
from Sprite import Sprite

class Ladder(Sprite):

    def __init__(self,x:int,y:int,map:int):
        super().__init__(x,y,(16,),(248,),(8,),(8,),map,1)

    def collision_box(self):
        ### ((x1,y1),(x2,y2)) ###

        ### (x1,y1)-------- ###
        ### |             | ###
        ### |             | ###
        ### |             | ###
        ### --------(x2,y2) ###
        return ((self.x,self.y),(self.x+8,self.y+8))
        