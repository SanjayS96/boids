from helpers import genlist, structure_vlist
from vect_ops_helpers import VectOps
import structure_ops
import numpy as np
from numpy.testing import assert_allclose
from timeit import timeit
import cProfile
import time

def benchmark(func): 
    def wrapper(*args): 
        t1 = time.time()
        ret = func(*args)
        t2 = time.time() 
        print(f'{func.__name__} | {round(t2-t1, 5)}s')
        return ret 
    
    return wrapper
# pr = cProfile.Profile()

def vops_initialize(): 
    fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
    vl = np.load(fn, allow_pickle=True)
    vops = VectOps(vl)

    return vops

class BenchVops(): 
    
    def __init__(self, vl): 
        fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
        # vl = np.load(fn, allow_pickle=True)

        self.vops = VectOps(vl)
    
    @benchmark
    def avg(self): 
        self._avg = self.vops.avg_pos()

    @benchmark
    def ali(self):
        self._align = self.vops.align()
    
    @benchmark
    def sep(self): 
        self._sep = self.vops.sep()

    @benchmark
    def vops_steer(self):
        self.vops.steer(self._avg)
        self.vops.steer(self._align)
        self.vops.steer(self._sep)
    
    @benchmark
    def cumtm(self): 
        self._avg = self.vops.avg_pos()
        self._align = self.vops.align()
        self._sep = self.vops.sep()        

        self.vops.steer(self._avg)
        self.vops.steer(self._align)
        self.vops.steer(self._sep)

class BenchStops(): 
    
    def __init__(self, vl): 
        fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
        # vl = np.load(fn, allow_pickle=True)
        
        self.stops = structure_ops.StructOps(vl)
    
    @benchmark
    def avg(self): 
        self._avg = self.stops.avg_pos()

    @benchmark
    def ali(self):
        self._align = self.stops.alignment()
    
    @benchmark
    def sep(self): 
        self._sep = self.stops.separate()

    @benchmark
    def stops_steer(self):
        self.stops.steer_debug(self._avg)
        self.stops.steer_debug(self._align)
        self.stops.steer_debug(self._sep)
    
    @benchmark
    def cumtm(self): 
        self._avg = self.stops.avg_pos()
        self._align = self.stops.alignment()
        self._sep = self.stops.separate()        

        self.stops.steer_debug(self._avg)
        self.stops.steer_debug(self._align)
        self.stops.steer_debug(self._sep)
    
def vops_bench():
    bv = BenchVops()
    bv.cumtm()

def stops_bench():
    bv = BenchStops()
    bv.cumtm()

vl = genlist(300)

BenchVops(vl).cumtm()
BenchStops(vl).cumtm()