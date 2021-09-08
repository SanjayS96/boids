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
    
    def __init__(self, graph_batch, maxspeed): 
        
        super().__init__(img, 0,0, batch =graph_batch)
        
        self.scale = 0.3
        
        self.velocity = np.zeros(2)
        self.acc = np.zeros(2)
        self.position = np.zeros(2)
        
        self.maxspeed = maxspeed

        
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

    def setup(self, n=10, maxspeed=12):
        self.batch = pyglet.graphics.Batch()
        self.s_list = [] 
        
        self.line_list = [] 
        self.stops = StructOps(n)
        self.stops.vlist['velocity'] += [1,1]
        for arr in self.stops.vlist:
            
            sprite = RefSprite(self.batch, maxspeed)

            sprite.position = arr['position']
            sprite.velocity = arr['velocity']
            sprite.acc = arr['acceleration']
            
            '''random colour'''
            # rng = np.random.default_rng()
            # r_color = rng.integers(0,255,3)
            # sprite.color = r_color 
            self.s_list.append(sprite)    
        self.stops.neighbour_distance = 100

    def setup_lines(self):            
        for s in self.s_list: 
            
            line = pyglet.shapes.Line(s.position[0],s.position[1], 0, 0, width=1, color = (0,255,0),batch=self.batch)
            self.line_list.append(line)
    def on_mouse_motion(self, x,y, dx, dy): 
        self.target = np.array([x,y])

        
    def draw_lines(self, dvs):
        for i, dv in enumerate(dvs): 
            np_xy = np.array(self.s_list[i].position)

            line = self.line_list[i]
            
            dv *= 100
            np_x2y2 = np_xy + dv 
            line.x2, line.y2 = np_x2y2

    def update(self, dt): 
        dvs = np.zeros(2)
        
        sf = np.zeros(2)
        # self.stops.non_mask_neighbours()
        # self.stops.nearby_neighbours()
        self.stops.recheck_neighbours()

        

        if self.target.any(): 
            dv = self.stops.steer_to_mouse(self.target)
            sf = self.stops.steer_debug(dv)

        avg = self.stops.avg_pos()
        align = self.stops.alignment()
        sep = self.stops.separate(40)
        
        # avg_sf = self.stops.steer_debug(avg, 0.04)
        # align_sf = self.stops.steer_debug(align, 0.04)

        # sf = avg_sf + align_sf
        # sep = self.stops.separate(desired_sep=50)
        # sep = self.stops.basic_sep(30)
        
        # align = self.stops.alignment()

        # if align.any():
        #     dvs += align
        sep*=0.01
        align *= 0.01
        dvs = avg *0.01 + align + sep 
        
        # dvs = avg + sep
        
        if self.target.any(): 
            pass
            # dvs += self.stops.steer_to_mouse(self.target) *6
            
        
        # avg*=0.3
        # align*=0.21
        # dvs *= 5
        # dvs -=  self.stops.vlist['velocity'] 
        # dvs *= 0.2


        self.stops.vlist['acceleration'] = dvs
        a = self.stops.vlist['velocity'].copy()
        self.stops.vlist['velocity'] += self.stops.vlist['acceleration']
        self.stops.limit_speed(2)
        
        self.stops.vlist['position'] += self.stops.vlist['velocity']

        self.stops.vlist['acceleration'] = np.zeros(2)

        r = self.stops.rotate()
        r = np.degrees(r)

        # self.stops.recheck_neighbours()
        
        breakpoint
        # self.stops.nearby_neighbours()
        for i, s in enumerate(self.s_list): 
            
        #     # if self.stops.vlist['position'][i].any():
            s.position = self.stops.vlist['position'][i]
            s.rotation = r[i]
            
            
            # s.position = self.stops.vlist[i]['position']

        self.stops.screen_wrap(self.dimension)

    def on_key_press(self, symbol, modifiers): 
        if symbol == ord('q'): 
            self.close()

        elif symbol == 65293: 
            self.update(0)
def main(): 
    w = GameWindow()
    w.setup(250, maxspeed=2)
    pyglet.clock.schedule_interval(w.update,1/144)
    # pyglet.clock.schedule_interval(w.update,1)
    # pyglet.clock.schedule_once(w.update,1/60)
    pyglet.app.run()
main()    


