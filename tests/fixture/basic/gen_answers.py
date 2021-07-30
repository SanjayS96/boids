


def calc_steering_forces():
    import numpy as np
    from vect_ops_helpers import VectOps
    from loader import load
    
    vlist = load()
    vops = VectOps(vlist)

    avg = vops.avg_pos()
    alignment = vops.align()
    sep = vops.sep()

    return avg, alignment, sep


