from helpers import genlist, structure_vlist
from vect_ops_helpers import VectOps
import structure_ops
import numpy as np
from numpy.testing import assert_allclose
from timeit import timeit
import cProfile, pstats, io
from pstats import SortKey
import time
np.set_printoptions(suppress=True)
def benchmark(func): 
    def wrapper(*args): 
        t1 = time.perf_counter()
        ret = func(*args)
        t2 = time.perf_counter() 
        # print(f'{func.__name__} | {round(t2-t1, 5)}s')
        print(f'{func.__name__} | {np.array([t2-t1])}s')
        return ret 
    
    return wrapper

def benchmark_timer(func): 
    def wrapper(*args): 
        t1 = time.perf_counter()
        ret = func(*args)
        t2 = time.perf_counter() 
        
        return ret, t2-t1
    
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


def generate(size):
    vl = genlist(size)
    name = f'tests\\test_env\\tests\\benchmarking\\vlist_{str(size)}'
    
    np.save(name, vl, allow_pickle=True) 

def cached_stops(size):
    '''returns StructOps instance with predefined structured 
    vlist'''
    
    try: 
        path=f'tests\\test_env\\tests\\benchmarking\\'
        name = f'{path}vlist_{str(size)}.npy'
        vl = np.load(name, allow_pickle=True)
    
        stops = structure_ops.StructOps(vl)

        struct_vl = stops.vlist
        struct_neighbours = stops.neighbours
        np.save(f'{path}struct_vlist_{str(size)}.npy', struct_vl, allow_pickle=True)
        np.save(f'{path}struct_neighbours{str(size)}.npy', struct_vl, allow_pickle=True)

    except FileNotFoundError:
        print('File not found')
    # vlist = 
    # np.save()


def predef_stops(): 
    vl = genlist(1)

    stops = structure_ops.StructOps(vl)
    
    path=f'tests\\test_env\\tests\\benchmarking\\'
    vlist = f'{path}struct_vlist_1000.npy'
    neighbours = f'{path}struct_vlist_1000.npy'
    stops.vlist = np.load(vlist, allow_pickle=True)
    stops.neighbours = np.load(neighbours, allow_pickle=True)

    return stops


def bench_sep(): 

    
    @benchmark
    def _genlist():
        vl = genlist(1000)

        return vl

    @benchmark
    def _structure(vl): 
        return structure_ops.StructOps(vl)
    @benchmark
    def _predef_structure():
        return predef_stops()

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

    s = predef_stops()
    sep = s.separate_bench_dict()

    def compare_mag():
        
        from numpy.core.umath_tests import inner1d
        diffs= s.faster_separate()
        @benchmark
        def mag1(): 
            return np.linalg.norm(diffs, axis=2)

        @benchmark
        def mag2():
            return np.sqrt(inner1d(diffs,diffs))

        @benchmark
        def mag3():
            # print(diffs.ndim)

            # v = np.array([300,500])
            # diffs = np.array([v for _ in range(10)])

            # print(diffs.ndim)
            # mag = np.linalg.norm(diffs, axis=1)
            einsum = np.einsum('ijk,ijk->ik', diffs, diffs)
            return einsum
            # print(mag,'\n', einsum)
        m1 = mag1()
        m2 = mag2()
        m3 = mag3()
        
        print(m1[0][1])
        # print(m3[0])
        print(m3)
        # assert_allclose(m1,m3)
    
    def mag_methods():
        
        vector = np.array([222.0, 194.0])

        @benchmark
        def _lin():
            return np.linalg.norm(vector)
        @benchmark
        def _dot():
            return np.sqrt(np.dot(vector, vector))
        
        @benchmark
        def _sum():
            return np.sqrt((vector*vector).sum(axis=0))

        @benchmark
        def _ein():
            return np.sqrt(np.einsum('i,i', vector, vector))

        @benchmark
        def _inn():
            return np.sqrt(np.inner(vector, vector))
        # fs = s.faster_separate()

            
        l = _lin()
        d = _dot()
        s = _sum()
        i = _inn()
        
        [assert_allclose(l,m) for m in [d,s,i]]
        
    
    
    def dict_print():
        
        pp = pprint.PrettyPrinter(indent=4)
        keys = sep.keys()
        vals = list(sep.values())
        longest=max([len(str(k)) for k in keys])
        sorted_sep = dict(sorted(sep.items(), key=lambda item: item[1]))
        
        for i,v in sep.items():
            print(i.ljust(longest,' '),': ',str(round(v,5)).ljust(5, ' '))

        sumtime = sum(list(sep.values())[:-1]) ##verify dict perfcounters by summing all

    dict_print()
bench_sep()
def profile_sep():
    pr = cProfile.Profile()
    pr.enable()

    so.separate()

    pr.disable()
    
    s = io.StringIO()
    sortby=SortKey.CUMULATIVE

    ps = pstats.Stats(pr).sort_stats(sortby)
    ps.strip_dirs().print_stats()



'''separation function is slowest in all cases'''
'''calculate algorithm scaling performance'''