from helpers import genlist, structure_vlist
from vect_ops_helpers import VectOps
import structure_ops
import numpy as np

fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
vl = np.load(fn, allow_pickle=True)

answers = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\answer_array.npy'
answer_array = np.load(answers, allow_pickle=True)

stops = structure_ops.StructOps(vl)
vlist = structure_vlist(vl)
cs_pos = stops.avg_pos()
cs_align= stops.alignment()

def test_check():
    assert np.allclose(cs_pos, answer_array[0])
    print('Position test passed')
    assert np.allclose(cs_align, answer_array[1])
    print('Alignment test passed')


