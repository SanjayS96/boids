from pyglet.sprite import Sprite
from pyglet.image import load
# from structure_ops import StructOps
# from helpers import genlist
import numpy as np 
# from arcade import sprite


def random_vects(n=10):
    from numpy.random import default_rng
    
    rvecs = [] 
    rng = default_rng()
    for i in range(n):
        rvec = rng.uniform(1,10,2)
        rvecs.append(rvec)

    return np.array(rvecs)

_img = r'C:\Users\Sanjay\code\projects\boids_2.0\src\resources\data\boid_sprite.png'
img = load(_img)

class RefSprite(Sprite): 
    
    def update(): 
        self.x, self.y = arr

    def __init__(self, arr): 
        self.arr = arr
        super().__init__(img, self.arr[0], self.arr[1], subpixel=True)
    
    # @property
    # def getx(self): 
    #     return self._x
    
    # @getx.setter
    # def setx(self,x): 
    #     self._x = x
    #     self._update_position()

    
class Value(object):
    def __init__(self, value): self.value = value

class Position(object):
    def __init__(self, value): 
        self.val_x = value[0]
        self.val_y = value[1]


class Parent(object): 
    def __init__(self,x,y):
        self.x, self.y = x,y

class Child(): 
    def __init__(self, data): 

        self.data = data        
        self.x = self.data[0]
        self.y = self.data[1]
        pass






breakpoint










