from helpers import genlist, structure_vlist
from vect_ops_helpers import VectOps
import structure_ops
import numpy as np
from numpy.testing import assert_allclose

fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
vl = np.load(fn, allow_pickle=True)

answers = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\answer_array2.npy'
answer_array = np.load(answers, allow_pickle=True)


vops = VectOps(vl)
stops = structure_ops.StructOps(vl)

def benchmark(func): 
    def wrapper(*args): 
        t1 = time.time()
        ret = func(*args)
        t2 = time.time() 
        # print(f'{func.__name__} took {t2-t1} seconds')
        return ret 
    
    return wrapper

def test_position():
    cs_pos = stops.avg_pos()
    assert np.allclose(cs_pos, answer_array[0])

def test_alignment():
    cs_align= stops.alignment()
    assert np.allclose(cs_align, answer_array[1])

def test_mags():
    diffs = vops.diffs()

    '''boilerplate for struct_ops diff testing, if necessary''' 
    pass

def standard_separation(): 
    cv = vl[0]

    sep_list = [] 
    for nearby in cv.nearby_vects: 
        dv = np.zeros(2)
        diff = cv.position - nearby.position
        mag = np.linalg.norm(diff)

        if mag.any(): 
            norm = diff / mag

            sep = None

def debug_compare(key_string, v_vals, s_vals, assertion = False):
    v_sort = v_vals[key_string]
    s_sort = s_vals[key_string][0]

    closeness = np.allclose(v_sort, s_sort)

    if not assertion: 
        return closeness

    assert closeness

def test_separation(): 
    

    def compare(key_string, output=True):
        v_sort = vsep[key_string]
        s_sort = sep[key_string][0]

        closeness = np.allclose(v_sort, s_sort)
        if output: 
            print(closeness)
            print('vector:\n', v_sort, '\nstruct:\n',s_sort)
        
        else: 
            return closeness

    des_sep = 200
    vops = VectOps(vl)
    
    
    vsep = vops.sep(des_sep)

    stops = structure_ops.StructOps(vl)
    sep = stops.separate(des_sep)
    
    assert_allclose(sep, vsep)


'''testing steer_force as sum of all forces'''

class TestAll(): 
    vl = np.load(fn, allow_pickle=True)
    vops = VectOps(vl)
    stops = structure_ops.StructOps(vl)

    def test_avg(self): 
        self.v_avg = self.vops.avg_pos()
        self.s_avg = self.stops.avg_pos()
        assert_allclose(self.v_avg, self.s_avg)

    def test_alignment(self): 
        self.v_align = self.vops.align()
        self.s_align = self.stops.alignment()

        assert_allclose(self.v_align, self.s_align)

    def test_separation(self): 
        self.v_sep = self.vops.sep(60)
        self.s_sep = self.stops.separate(60)

        assert_allclose(self.v_sep, self.s_sep)
    
    def test_steering(self): 
        '''for simplicity, just test steering 
        toward one force (avg_pos)'''
        v_avg = self.vops.avg_pos()
        s_avg = self.stops.avg_pos()
        
        v_align = self.vops.align()
        s_align = self.stops.alignment()
        
        v_sep = self.vops.sep(60)
        s_sep = self.stops.separate(60)
        
        v_steer_avg = self.vops.steer_debug(v_avg)
        s_steer_avg = self.stops.steer_debug(s_avg)
        
        v_steer_align = self.vops.steer_debug(v_align)
        s_steer_align = self.stops.steer_debug(s_align)

        v_steer_sep = self.vops.steer_debug(v_sep)
        s_steer_sep = self.stops.steer_debug(s_sep)
        breakpoint
        assert_allclose(v_steer_avg, s_steer_avg)
        assert_allclose(v_steer_align, s_steer_align)
        assert_allclose(v_steer_sep, s_steer_sep)

        v_vels = vops.steer(v_avg, 0, 0)

        vl = np.load(fn, allow_pickle=True)
        stops = structure_ops.StructOps(vl)

        s_vels = stops.steer_to_dv(s_avg)
        
        assert_allclose(v_vels, s_vels)

TestAll().test_steering()
breakpoint

