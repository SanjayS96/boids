from structure_ops import StructOps
import numpy as np 
from benchmarking import benchmark_timer
import warnings
from scipy import spatial

warnings.filterwarnings('ignore')
np.set_printoptions(suppress=True)
fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
vl = np.load(fn, allow_pickle=True)


stops = StructOps(vl)
diffs = stops.faster_separate()

from numpy.core.umath_tests import inner1d

def stand_mag():
    mags = np.linalg.norm(diffs, axis=2)
    return mags

def inn1d_mag():
    return np.sqrt(inner1d(diffs,diffs))

def stan_inner(): 
    # d = diffs[...:0:]

    # d = np.take_along_axis(diffs, axis=2)
    d = diffs[0,0,:]

    sm = stand_mag()

    
def dot(): 
    d = np.dot(diffs,diffs)

def ein(): 
    return np.sqrt(np.einsum('ijk,ijk->ij', diffs, diffs))

class Timer(): 
    def __init__(self, func): 
        self.values, self.time = self.function(func) 
        self.name = func.__name__
        
    @benchmark_timer
    def function(self, func):
        return func() 




m1 = Timer(stand_mag)
m2 = Timer(inn1d_mag)
m3 = Timer(ein)


def poll_results(*timers):
    
    times = [t.time for t in timers]
    names = [t.name for t in timers]

    sorted_times = sorted(times)
    sorted_names = []
    
    for st in sorted_times: 
        t_index = times.index(st)
        sorted_names.append(names[t_index])

    sorted_times = np.array(sorted_times)
    
    slowest = sorted_times[-1]
    percentage = slowest/sorted_times

    percentage = np.around(percentage, 2)

    st_column = sorted_times[:,np.newaxis]
    sn_column = np.array(sorted_names)[:,np.newaxis]

    for i in range(st_column.size): 
        print(sn_column[i][0], st_column[i], percentage[i])

    # print(np.allclose(m1.values[0], m2.values[0]))
    '''missing value assertation '''
    
poll_results(m1,m2,m3)

# print(m3.values)
# print(np.allclose(sm, m3.values))

breakpoint







