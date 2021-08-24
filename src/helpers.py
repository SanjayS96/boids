import numpy as np

def genlist(n): 

    from vect import Vector
    l = np.array([Vector() for i in range(n)])

    return l

def structure_vlist(vect_list):
    data = [] 
    for vect in vect_list:

        vector = (vect.position.copy(), vect.acc.copy(), vect.velocity.copy(), vect.maxspeed)
        data.append(vector)
    
    dt = np.dtype([('position', 'f8', (2,)), ('acceleration','f8', (2,)), ('velocity','f8', (2,)), ('maxspeed', 'f8', (1,))])
    vector_list = np.array(data, dtype=dt)
    
    return vector_list


def benchmark2(func): 
    import time
    def wrapper(*args, runs=1):
        t1 = time.time()
        for i in range(runs): 
            ret = func(*args)
        t2 = time.time() 
        print(f'{func.__name__} took {t2-t1} seconds')
        return ret

    return wrapper

def column_compare(result1, result2): 
    list1 = result1.tolist()
    list2 = list_2.tolist()

    assert((len(list1) == len(list2)))
    for i in range(len(list1) -1):
        print(f'{list1[i]} | {list2[i]} \n')