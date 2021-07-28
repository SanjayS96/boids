from src.vect import Vector
from src.helpers import genlist, structure_vlist, benchmark2, column_compare
from src.vect_ops_helpers import VectOps
import src.structure_ops as stops
import numpy as np

avg_pos_list = []
vlist = genlist(5)
struct_vlist = structure_vlist(vlist)

test_array = np.arange(5)

@benchmark2
def bench():
    n = stops.neighbours(test_array)

vops = VectOps(vlist)

def close(*args):
    return np.allclose(*args)

n = stops.neighbours(vlist)
n1 = stops.neighbours(struct_vlist)
neighbours,vects = stops.neighbours2(struct_vlist)

def non_norm_avg_test():
    v_avg = vops.non_norm_avg()
    s_avg = stops.non_norm_avg(struct_vlist, neighbours)
    assert close(v_avg, s_avg)


def dv_mag_test():
    v_dv, v_mags = vops.dv_test()
    s_dv, s_mags = stops.avg_pos(struct_vlist, neighbours)

    assert close(v_dv, s_dv)
    assert close(v_mags, s_mags)

def pos_test():
    
    v_avg = vops.avg_pos()
    s_avg = stops.avg_pos(struct_vlist, neighbours)

    assert close(v_avg, s_avg)
    return s_avg

s_align = stops.alignment(neighbours)
v_align = vops.align()

v_sep = vops.sep(900)

svpos = (struct_vlist['position'])
npos = (neighbours['position'])


svpos = (struct_vlist['position'])
# print(svpos.shape)

svpos = svpos[:,np.newaxis]
diffs = svpos-npos