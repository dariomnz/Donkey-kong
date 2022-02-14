import pyxel
from Sprite import Sprite


class Mario(Sprite):
    """Clase del personaje"""
    
    def __init__(self,x:int,y:int):
        """Cronstructor de el personaje"""

        ### Tamaño y ubicacion de las imagenes ###
        self.width_image_map=( 12,15,15,13,16,          16 ,13 ,15 ,15 ,12)
        self.height_image_map=(16,16,15,16,15,          15 ,16 ,15 ,16 ,16)
        self.x_image_map=(     0 ,12,27,42,55,          177,193,206,221,236)
        self.y_image_map=(     0 ,0 ,0 ,0 ,0 ,          0  ,0  ,0  ,0  ,0)

        ### Variables para el control del movimiento ###
        self.RIGHT=0
        self.LEFT=0
        self.UP=0
        self.DOWN=0
        self.vel_x=2
        self.vel_y=1

        ### Variables para clim ###
        self.isClimbing=False

        ### Variables necesarias para el salto ###
        self.isJumping_UP=False
        self.isJumping_DOWN=False
        self.init_time_jump=0

        ### Variables para la animacion ###
        self.animation={
        'IDLE_LEFT':0,'IDLE_RIGHT':-1,
        'WALK_LEFT1':1,'WALK_LEFT2':2,
        'WALK_RIGHT1':-2,'WALK_RIGHT2':-3,
        'CLIMB1':3,'CLIMB2':-4,
        'JUMP_LEFT':4,'JUMP_RIGHT':-5}
        self.current_animation='IDLE_RIGHT'

        ### Constructor del padre ###
        Sprite.__init__(self,x,y,
        self.x_image_map,
        self.y_image_map,
        self.width_image_map,
        self.height_image_map,
        1)
        

    def draw(self):
        Sprite.draw(self)


    def update(self):
        ### Contador de la imagen de la animacion ###
        self.counter=self.get_counter_animation()
        
        ### Cambio de Jumping a dejar de slatar ###
        if self.isJumping_UP:
            if pyxel.frame_count-self.init_time_jump>7:
                self.isJumping_UP=False
                self.init_time_jump=pyxel.frame_count
                self.isJumping_DOWN=True
        if self.isJumping_DOWN:
            if pyxel.frame_count-self.init_time_jump>7:                
                self.isJumping_DOWN=False
        ### Correcction de la posicion para que no se salga de la pantalla ###
        if self.x>256-self.width_image_map[self.counter]:
            self.x=256-self.width_image_map[self.counter]
        if self.x<0:
            self.x=0
        if self.y>256-self.height_image_map[self.counter]:
            self.y=256-self.height_image_map[self.counter]
        if self.y<0:
            self.y=0
                

            
    def get_counter_animation(self)->int:
        """ Devuelve el numero de la imagen que debe pintarse """
        if pyxel.frame_count%3==0:
            ## Ciclos de walk ##
            if self.RIGHT-self.LEFT>0:
                ## Ciclo walk_right ##
                if self.current_animation=='IDLE_RIGHT':
                    self.current_animation='WALK_RIGHT1'
                elif self.current_animation=='WALK_RIGHT1':
                    self.current_animation='WALK_RIGHT2'
                elif self.current_animation=='WALK_RIGHT2':
                    self.current_animation='IDLE_RIGHT'
                ## Cambio de sentido ##
                elif self.current_animation=='IDLE_LEFT':
                    self.current_animation='IDLE_RIGHT'
                elif self.current_animation=='WALK_LEFT1':
                    self.current_animation='IDLE_RIGHT'
                elif self.current_animation=='WALK_LEFT2':
                    self.current_animation='IDLE_RIGHT'
                
            elif self.RIGHT-self.LEFT<0:
                ## Ciclo walk_left ##
                if self.current_animation=='IDLE_LEFT':
                    self.current_animation='WALK_LEFT1'
                elif self.current_animation=='WALK_LEFT1':
                    self.current_animation='WALK_LEFT2'
                elif self.current_animation=='WALK_LEFT2':
                    self.current_animation='IDLE_LEFT'
                ## Cambio de sentido ##
                elif self.current_animation=='IDLE_RIGHT':
                    self.current_animation='IDLE_LEFT'
                elif self.current_animation=='WALK_RIGHT1':
                    self.current_animation='IDLE_LEFT'
                elif self.current_animation=='WALK_RIGHT2':
                    self.current_animation='IDLE_LEFT'
            ## Animacion de climb ##
            #if self.isClimbing:
            if self.DOWN-self.UP!=0:
                if self.current_animation=='CLIMB2':
                    self.current_animation='CLIMB1'
                elif self.current_animation=='CLIMB1':
                    self.current_animation='CLIMB2'
        ## Cambio a idle, cuando no hay velocidad ##
        if self.RIGHT-self.LEFT==0:
            if self.current_animation=='WALK_RIGHT1':
                self.current_animation='IDLE_RIGHT'
            elif self.current_animation=='WALK_RIGHT2':
                self.current_animation='IDLE_RIGHT'
            elif self.current_animation=='WALK_LEFT1':
                self.current_animation='IDLE_LEFT'
            elif self.current_animation=='WALK_LEFT2':
                self.current_animation='IDLE_LEFT'
        ## Climb ##
        if self.isClimbing:
            ## Cambio de walk-idle a climb ##
            if self.current_animation=='IDLE_LEFT':
                self.current_animation='CLIMB1'
            elif self.current_animation=='WALK_LEFT1':
                self.current_animation='CLIMB1'
            elif self.current_animation=='WALK_LEFT2':
                self.current_animation='CLIMB1'
            elif self.current_animation=='IDLE_RIGHT':
                self.current_animation='CLIMB1'
            elif self.current_animation=='WALK_RIGHT1':
                self.current_animation='CLIMB1'
            elif self.current_animation=='WALK_RIGHT2':
                self.current_animation='CLIMB1'
        else:
            ## Cambio de climb a idle ##
            if self.current_animation=='CLIMB2':
                self.current_animation='IDLE_LEFT'
            elif self.current_animation=='CLIMB1':
                self.current_animation='IDLE_RIGHT'
        ## Cambio a jump desde idle-walk ##
        if self.isJumping_UP or self.isJumping_DOWN:
            if self.RIGHT-self.LEFT>0:
                self.current_animation='JUMP_RIGHT'
            else:
                self.current_animation='JUMP_LEFT'
        else:
            if self.current_animation=='JUMP_LEFT':
                self.current_animation='IDLE_LEFT'
            elif self.current_animation=='JUMP_RIGHT':
                self.current_animation='IDLE_RIGHT'
        
        return self.animation.get(self.current_animation)


    def collision_box(self) -> tuple:
        ### ((x1,y1),(x2,y2)) ###

        ### (x1,y1)-------- ###
        ### |             | ###
        ### |             | ###
        ### |             | ###
        ### --------(x2,y2) ###
        return ((self.x+2,self.y+14),(self.x+11,self.y+15))
