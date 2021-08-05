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
n = structure_ops.neighbours(vlist)

s_pos = structure_ops.avg_pos(vlist, n)
cs_pos = stops.avg_pos()
cs_align= stops.alignment()
s_align = structure_ops.alignment(n)

def check():
    assert np.allclose(cs_pos, answer_array[0])
    assert np.allclose(cs_align, answer_array[1])




