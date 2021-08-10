from helpers import genlist, structure_vlist
from vect_ops_helpers import VectOps
import structure_ops
import numpy as np

fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
vl = np.load(fn, allow_pickle=True)

answers = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\answer_array.npy'
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

def test_separation(): 
    cs_diffs = stops.separate()
    diffs = vops.diffs()

    assert np.allclose(cs_diffs, diffs) #position test

    standard_mag = []
    for d in diffs: 
        standard_mag.append(np.linalg.norm(d, axis=1))
    

    cs_mag = np.linalg.norm(cs_diffs, axis=2)
    assert np.allclose(cs_mag, standard_mag) #magnitude test

    


test_separation()