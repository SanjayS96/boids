import numpy as np 




# existing_arr = exists(r'C:/Users/Sanjay/')


'''move arrays to setup.py pkg_resources 
to ensure test env is isolated''' 

def generate_new(n=50):
    from vect_ops_helpers import VectOps
    from helpers import genlist
    from os import getcwd
    from os.path import exists, join 
    
    vl = genlist(n)
    path = f'{getcwd()}\\tests\\fixture\\basic\\basic_context_array'
    print(path)
    np.save(path, vl, allow_pickle=True)
