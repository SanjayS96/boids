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

    raise NotImplementedError

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
from copy import deepcopy
vl_copy = deepcopy([v.velocity for v in vl])
def test_all():

    v_steering = vops.steer()

    assert_allclose(stops.vlist['velocity'], vl_copy)

    #reset vl
    vl = np.load(fn, allow_pickle=True)

    avg = stops.avg_pos()
    align = stops.alignment()
    sep = stops.separate()

    dvs = np.array((avg, align, sep))
    
    stops.steer_to_dv(avg)
    # stops.steer_to_dv(align)
    # stops.steer_to_dv(sep)

    s_steering = stops.vlist['velocity']

    return v_steering, s_steering
test_all()

breakpoint

