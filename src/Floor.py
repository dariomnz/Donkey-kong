import pyxel
from Sprite import Sprite

class Floor(Sprite):
    
    def __init__(self,x:int,y:int,map:int):
        Sprite.__init__(self,x,y,(0,),(248,),(16,),(8,),map,1)


    def collision_box(self):
        ### ((x1,y1),(x2,y2)) ###

        ### (x1,y1)-------- ###
        ### |             | ###
        ### |             | ###
        ### |             | ###
        ### --------(x2,y2) ###
        return ((self.x,self.y),(self.x+16,self.y+8))