def generate_answers():
    
    from helpers import genlist, structure_vlist
    from vect_ops_helpers import VectOps
    import structure_ops
    import numpy as np
    
    file_name = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\answer_array2.npy'
    vl = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'

    vlist = np.load(vl, allow_pickle=True)
    vops = VectOps(vlist)

    pos = vops.avg_pos()
    align = vops.align()
    sep = vops.sep()

    answer_array = np.array([pos,align,sep])
    np.save(file_name, answer_array, allow_pickle=True)
