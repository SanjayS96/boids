from helpers import genlist, structure_vlist
from vect_ops_helpers import VectOps
import structure_ops
import numpy as np
from numpy.testing import assert_allclose
from timeit import timeit
import cProfile, pstats, io
from pstats import SortKey
import time

def benchmark(func): 
    def wrapper(*args): 
        t1 = time.perf_counter()
        ret = func(*args)
        t2 = time.perf_counter() 
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
    
def vops_bench(vl):
    bv = BenchVops(vl)
    
    bv.avg()
    bv.ali()
    bv.sep()

    bv.vops_steer()
    #bv.cumtm()

def stops_bench(vl):
    bs = BenchStops(vl)
    
    bs.avg()
    bs.ali()
    bs.sep()
    
    bs.stops_steer()
    #bv.cumtm()

def main_bench():
    vl = genlist(500)

    vops_bench(vl)
    stops_bench(vl)


def bench_sep(): 

    
    @benchmark
    def _genlist():
        vl = genlist(1000)

        return vl

    @benchmark
    def _structure(vl): 
        return structure_ops.StructOps(vl)
    vl= _genlist()

    s = _structure(vl)

    '''
    initializing structops is slow. 
    takes just as long as sep.
    probably slow because it copies the vector data individually. 
    
    possible fix: copy/deepcopy vectorlist in its entirety, then have
    structops init directly assign attrs from vl. 
    NOTE: that might break pyglet sprite's inheritence from array. testing required.
    '''

    
    @benchmark
    def norm_sep(): 
        return s.separate()
    
    @benchmark
    def avg():
        return s.avg_pos()
    @benchmark
    def fast_sep():
        return s.faster_separate()

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    st = time.perf_counter()
    sep =s.separate_bench_dict()
    

    
    keys = sep.keys()
    vals = list(sep.values())
    longest=max([len(str(k)) for k in keys])
    
    sep = dict(sorted(sep.items(), key=lambda item: item[1]))

    for i,v in sep.items():
        print(i.ljust(longest,' '),': ',str(round(v,5)).ljust(5, ' '))

    sumtime = sum(list(sep.values())[:-1])
    print(time.perf_counter() - st)

    np_vals = np.array(vals)
    

def profile_sep():
    pr = cProfile.Profile()
    pr.enable()

    so.separate()

    pr.disable()
    
    s = io.StringIO()
    sortby=SortKey.CUMULATIVE

    ps = pstats.Stats(pr).sort_stats(sortby)
    ps.strip_dirs().print_stats()


t = time.time()
bench_sep()
print(time.time() - t)
'''separation function is slowest in all cases'''
'''calculate algorithm scaling performance'''