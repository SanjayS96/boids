from pyglet.sprite import Sprite
from pyglet.image import load

import pyglet
from structure_ops import StructOps
from helpers import genlist, structure_vlist
import numpy as np 
from numpy.random import default_rng
# from arcade import sprite



def random_vects(n=10):
    from numpy.random import default_rng
    
    rvecs = [] 
    rng = default_rng()
    for i in range(n):
        rvec = rng.integers(1,10,2)
        rvecs.append(rvec)

    return np.array(rvecs)

_img = r'C:\Users\Sanjay\code\projects\boids_2.0\src\resources\data\boid_sprite.png'
img = load(_img)

img.anchor_x, img.anchor_y = 25,25

class RefSprite(Sprite): 
    
    def __init__(self, graph_batch): 
        
        super().__init__(img, 0,0, batch =graph_batch)
        
        self.scale = 0.21
        
        self.velocity = np.zeros(2)
        self.acc = np.zeros(2)
        self.position = np.zeros(2)
        
        self.maxspeed = 6

        
    def applyForces(self): 
        self.velocity += self.acc
        self.position += self.velocity
        self.acc = np.zeros(2)

class GameWindow(pyglet.window.Window):
    def __init__(self): 
        
        win_w,win_h = 800,800
        self.dimension = np.array([win_w,win_h])
        super().__init__(win_w,win_h)
        screen_w,screen_h = 1920,1080 
        
        #centering window
        w = (screen_w - win_w)//2
        h = (screen_h - win_h)//2

        self.set_location(w,h)
        self.circles = []

        
        self.target = np.zeros(2)
        self.fps = pyglet.window.FPSDisplay(window=self)
    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.fps.draw()

        # if self.circles:
        #     for circle in self.circles:
        #         circle.draw()
        
        # self.line.draw() 
        # for s in self.s_list: 
        #     s.draw()

    def setup(self, n=10):
        self.batch = pyglet.graphics.Batch()
        self.s_list = [] 
        
        self.line_list = [] 
        self.stops = StructOps(n)
        for arr in self.stops.vlist:
            
            sprite = RefSprite(self.batch)
            sprite.position = arr['position']
            sprite.velocity = arr['velocity']
            sprite.acc = arr['acceleration']
            self.s_list.append(sprite)    


    def on_mouse_motion(self, x,y, dx, dy): 
        self.target = np.array([x,y])

    def update(self, dt): 
        

        # self.stops.nearby_neighbours()
        pass
        breakpoint
        # self.stops.nearby_neighbours()

    def on_key_press(self, symbol, modifiers): 
        ENTER = 65293
        if symbol == ord('q'): 
            self.close()

        elif symbol == ENTER: 
            print(self.stops.neighbours['position'].)

            
            
            
            # print(mask_data)

def main(): 
    w = GameWindow()
    w.setup(5)
    pyglet.clock.schedule_interval(w.update,1/144)
    # pyglet.clock.schedule_interval(w.update,1)
    # pyglet.clock.schedule_once(w.update,1/60)
    pyglet.app.run()

main()