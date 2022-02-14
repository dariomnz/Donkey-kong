import pyxel

from Sprite import Sprite
from Mario import Mario
from Donkey import  Donkey
from Barrel import Barrel
from Static_Barrel import Static_Barrel
from Floor import Floor
from Ladder import  Ladder


class App(object):
    def __init__(self,widht: int,height:int):
        ### Inicia la aplicacion ###
        pyxel.init(widht,height,)
        ### Lista con todos los sprites ###
        self.start()
        ### boolean que controla la funcion de pausa ###
        self.pausa=False
        ### String que almacena los comandos ###
        self.command_line=""
        ### Mapa en el que se esta actualmente
        self.map=1
        ### Puntos del jugador ###
        self.points=0
        ### Tiempo entre punto y punto ###
        self.time_for_point=00
        ### Grabedad del juego en pixeles por frame ###
        self.gravity=3
        ### Carga al banco de imagenes el assetsmap ###
        pyxel.image(1).load(0,0,"../assets/assetsmap.png")
        ### Hace que se muestre el raton por pantalla ###
        pyxel.mouse(True)

        ### Esconde los sprites que no pertenecen al mapa 1 ###
        for i in self.sprites:
            if i.map!=1:
                i.isEnable=False
            else:
                i.isEnable=True
        
        ### Inicia el bucle infinito de update y de draw ###
        pyxel.run(self.update,self.draw)

    def update(self):

        if self.pausa:
            ### Juego en pausa ###
            aux_string=self.input_command()
            if aux_string=='delete':
                self.command_line=self.command_line[:-1]
            else:
                self.command_line+=aux_string
            
            if pyxel.btnp(pyxel.KEY_RSHIFT):
                self.pausa=False  
                self.command_line=""  
            ### Para ejecutar los comandos ###
            if pyxel.btnp(pyxel.KEY_RETURN):
                if(self.command_line=="map1"):
                    for i in self.sprites:
                            if i.map!=1:
                                i.isEnable=False
                            else:
                                i.isEnable=True
                if(self.command_line=="map0"):
                    for i in self.sprites:
                            if i.map!=0:
                                i.isEnable=False
                            else:
                                i.isEnable=True
                self.command_line=""  
                self.pausa=False          
        else:
            ### Juego corriendo normal ###

            ### Para poner el modo pausa ###
            if pyxel.btnp(pyxel.KEY_RSHIFT):
                self.pausa=True  
            
            ### Movimiento del jugador ###
            
            if pyxel.btnp(pyxel.KEY_A):
                self.player.LEFT=1
            if pyxel.btnr(pyxel.KEY_A):
                self.player.LEFT=0
            if pyxel.btnp(pyxel.KEY_D):
                self.player.RIGHT=1
            if pyxel.btnr(pyxel.KEY_D):
                self.player.RIGHT=0
            
            if pyxel.btnp(pyxel.KEY_W):
                self.player.UP=1
            if pyxel.btnr(pyxel.KEY_W):
                self.player.UP=0
            if pyxel.btnp(pyxel.KEY_S):
                self.player.DOWN=1
            if pyxel.btnr(pyxel.KEY_S):
                self.player.DOWN=0
            
            ### Salto del jugador ###
            if not (self.player.isJumping_UP or self.player.isJumping_DOWN) and not self.player.isClimbing:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.player.isJumping_UP=True
                    self.player.init_time_jump=pyxel.frame_count
            
            ### Creacion de barriles ###
            if pyxel.frame_count%60==0:
                self.sprites.append(Barrel(self.monkey.x+13,self.monkey.y+15))

            ### Update de todos los sprites ###
            for i in self.sprites:
                if i.isEnable:
                    i.update()

                    if type(i)==Mario:
                        ### Movimiento del jugador ###
                        increment_x=0
                        increment_y=0
                        ### Movimiento en x ###
                        increment_x=self.player.vel_x*(self.player.RIGHT-self.player.LEFT)
                        ### Movimiento en y ###
                        ## Para el salto ##
                        if self.player.isJumping_UP:
                            increment_y=-2
                        elif self.player.isJumping_DOWN:
                            increment_y=2
                        else:
                        ## Para cuando esta climbing ##    
                            if self.anyCollision_ladders(i):                            
                                increment_y=self.player.vel_y*(self.player.DOWN-self.player.UP)
                                if increment_y!=0:
                                    self.player.isClimbing=True
                            else:
                        ## Cuando esta normal, la y solo es afectada por la gravedad ##
                                increment_y=self.gravity
                                self.player.isClimbing=False

                        self.incrementMove(self.player,increment_x,increment_y)                        

                    if type(i)==Barrel:
                        ### Colision con el jugador ###
                        if i.point_collision(self.player)and pyxel.frame_count-self.time_for_point>4:
                            self.time_for_point=pyxel.frame_count
                            self.points+=100

                        if i.collision(self.player):
                            self.start()
                            
                        ### Movimiento del barril ###
                        increment_x=i.vel_x*(i.RIGHT-i.LEFT)
                        increment_y=self.gravity
                        self.incrementMove(i,increment_x,increment_y)

                        if i.y>244:
                            self.sprites.remove(i)


        
    def draw(self):
            ### Limpiado de pantalla ###
            pyxel.cls(0)
            
            ### Puntos del jugador ###
            pyxel.text(39,10,str(self.points),7)
            ### Draw de todos los sprites ###
            for i in self.sprites:
                if i.isEnable:
                    i.draw()

            ### Dibuja la barra de comandos del modo pausa ###
            if self.pausa:
                pyxel.rect(0,236,256,20,1)
                pyxel.text(0,243,self.command_line,7)


    def incrementMove(self,sprite:Sprite,plus_x:int,plus_y:int) -> None:
        """ Funcion para mover el Sprite seleccionado, teniendo en cuenta las colisiones """
        if type(sprite)==Mario:
            if plus_x>0:
                step_for=1
            else:
                step_for=-1

            for step in range (0,plus_x+step_for,step_for):
                sprite.x+=step
                if step!=plus_x:
                    if self.anyCollision_floors(sprite):
                        if not (sprite.isJumping_UP or sprite.isJumping_DOWN):
                            sprite.y-=self.gravity+1
                        sprite.x-=step_for
                        break
                    else:
                        sprite.x-=step

            if plus_y>0:
                step_for=1
            else:
                step_for=-1

            for step in range (0,plus_y+step_for,step_for):
                sprite.y+=step
                if step!=plus_y:
                    if plus_y>0 or self.player.isJumping_UP or self.player.isJumping_DOWN:
                        if self.anyCollision_floors(sprite):
                            sprite.y-=step_for
                            break
                        else:
                            sprite.y-=step
                    else:

                        sprite.y-=step
        else:
            if plus_x>0:
                step_for=1
            else:
                step_for=-1

            for step in range (0,plus_x+step_for,step_for):
                sprite.x+=step
                if step!=plus_x:
                    if self.anyCollision_floors(sprite):
                        sprite.y-=self.gravity+1
                        sprite.x-=step_for
                        break
                    else:
                        sprite.x-=step

            if plus_y>0:
                step_for=1
            else:
                step_for=-1

            for step in range (0,plus_y+step_for,step_for):
                sprite.y+=step
                if step!=plus_y:
                    if plus_y>0:
                        if self.anyCollision_floors(sprite):
                            sprite.y-=step_for
                            break
                        else:
                            sprite.y-=step
                    else:

                        sprite.y-=step


    def anyCollision_floors(self,sprite:Sprite) -> bool:
        """ Comprueba todas las colisiones del sprite introducido, con todos los floors """
        exit=False
        for i in self.sprites:
            if i.isEnable:
                if type(i)==Floor:
                    if(sprite.collision(i)):
                        exit=True    
                        break
        return exit


    def anyCollision_ladders(self,sprite:Sprite) -> bool:
        """ Comprueba la colision del sprite introducido, con todos los ladders """
        exit=False
        for i in self.sprites:
            if type(i)==Ladder:
                if(sprite.collision(i)):
                    exit=True    
                    break
        return exit

        
    def input_command(self) -> str:
        #print(self.command_line)
        """ Devuelve la letra correspondiente a la tecla pulsada por teclado """
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            return 'delete'
        if pyxel.btnp(pyxel.KEY_0):
            return '0'
        if pyxel.btnp(pyxel.KEY_1):
            return '1'
        if pyxel.btnp(pyxel.KEY_2):
            return '2'
        if pyxel.btnp(pyxel.KEY_3):
            return '3'
        if pyxel.btnp(pyxel.KEY_4):
            return '4'
        if pyxel.btnp(pyxel.KEY_5):
            return '5'
        if pyxel.btnp(pyxel.KEY_6):
            return '6'
        if pyxel.btnp(pyxel.KEY_7):
            return '7'
        if pyxel.btnp(pyxel.KEY_8):
            return '8'
        if pyxel.btnp(pyxel.KEY_9):
            return '9'
        if pyxel.btnp(pyxel.KEY_A):
            return 'a'
        if pyxel.btnp(pyxel.KEY_B):
            return 'b'
        if pyxel.btnp(pyxel.KEY_C):
            return 'c'
        if pyxel.btnp(pyxel.KEY_D):
            return 'd'
        if pyxel.btnp(pyxel.KEY_E):
            return 'e'
        if pyxel.btnp(pyxel.KEY_F):
            return 'f'
        if pyxel.btnp(pyxel.KEY_G):
            return 'g'
        if pyxel.btnp(pyxel.KEY_H):
            return 'h'
        if pyxel.btnp(pyxel.KEY_I):
            return 'i'
        if pyxel.btnp(pyxel.KEY_J):
            return 'j'
        if pyxel.btnp(pyxel.KEY_K):
            return 'k'
        if pyxel.btnp(pyxel.KEY_L):
            return 'l'
        if pyxel.btnp(pyxel.KEY_M):
            return 'm'
        if pyxel.btnp(pyxel.KEY_N):
            return 'n'
        if pyxel.btnp(pyxel.KEY_O):
            return 'o'
        if pyxel.btnp(pyxel.KEY_P):
            return 'p'
        if pyxel.btnp(pyxel.KEY_Q):
            return 'q'
        if pyxel.btnp(pyxel.KEY_R):
            return 'r'
        if pyxel.btnp(pyxel.KEY_S):
            return 's'
        if pyxel.btnp(pyxel.KEY_T):
            return 't'
        if pyxel.btnp(pyxel.KEY_U):
            return 'u'
        if pyxel.btnp(pyxel.KEY_V):
            return 'v'
        if pyxel.btnp(pyxel.KEY_W):
            return 'w'
        if pyxel.btnp(pyxel.KEY_X):
            return 'x'
        if pyxel.btnp(pyxel.KEY_Y):
            return 'y'
        if pyxel.btnp(pyxel.KEY_Z):
            return 'z'
        return ""
        
        

    def start(self):
        ### Espacio de crear los sprites ###
        self.points=0
        self.sprites=list()

        floor_map1=(
            (16,240),(32,240),(48,240),(64,240),(80,240),(96,240),(112,240),(128,239),(144,238),(160,237),(176,236),(192,235),(208,234),(224,233),
            (16,200),(32,201),(48,202),(64,203),(80,204),(96,205),(112,206),(128,207),(144,208),(160,209),(176,210),(192,211),(208,212),
            (32,179),(48,178),(64,177),(80,176),(96,175),(112,174),(128,173),(144,172),(160,171),(176,170),(192,169),(208,168),(224,167),
            (16,134),(32,135),(48,136),(64,137),(80,138),(96,139),(112,140),(128,141),(144,142),(160,143),(176,144),(192,145),(208,146),
            (32,113),(48,112),(64,111),(80,110),(96,109),(112,108),(128,107),(144,106),(160,105),(176,104),(192,103),(208,102),(224,101),
            (16,76),(32,76),(48,76),(64,76),(80,76),(96,76),(112,76),(128,76),(144,76),(160,77),(176,78),(192,79),(208,80),
            (104,48),(120,48),(136,48)
        )

        floor_map0=(
            (16,200),(16,200),(32,201),(48,202),(64,203),(80,204),(96,205),(112,206),(128,207),(144,208),(160,209),(176,210),(192,211),(208,212),
        )

        ladders_map=(
            (96,232),(96,208),   (200,228),(200,220),(200,212),
            (48,196),(48,188),(48,180),       (112,200),(112,192),(112,184),(112,176),    
            (80,168),(80,144),      (128,168),(128,160),(128,152),(128,144),      (200,164),(200,156),(200,148),
            (48,128),(48,120),      (88,132),(88,124),(88,116),       (184,136),(184,112),
            (104,104),(104,96),(104,80),    (200,96),(200,88),(200,80),
            (80,72),(80,64),(80,56),(80,48),(80,40),(80,32),(80,24),  (96,72),(96,64),(96,56),(96,48),(96,40),(96,32),(96,24),  (144,72),(144,64),(144,56)
        )

        self.sprites.append(Sprite(40,1,(155,),(249,),(22,),(7,),1))
        self.sprites.append(Sprite(87,1,(177,),(249,),(79,),(7,),1))

        for i in range(len(ladders_map)):
            self.sprites.append(Ladder(ladders_map[i][0],ladders_map[i][1],1))

        for i in range(len(floor_map1)):
            self.sprites.append(Floor(floor_map1[i][0],floor_map1[i][1],1))

        for i in range(len(floor_map0)):
            self.sprites.append(Floor(floor_map0[i][0],floor_map0[i][1],0))

        #sprites.append(Barrel(10,10))

        self.sprites.append(Static_Barrel(16,60))
        self.sprites.append(Static_Barrel(26,60))
        self.sprites.append(Static_Barrel(16,44))
        self.sprites.append(Static_Barrel(26,44))

        self.sprites.append(Donkey(39,44))
        self.monkey=self.sprites[-1]
        self.sprites.append(Mario(20,220))
        self.player=self.sprites[-1]


App(256,256)