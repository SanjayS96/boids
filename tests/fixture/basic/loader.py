def load():
    import numpy as np 
    import os
    cwd = os.getcwd()
    arr_path = r'tests\fixture\basic\basic_context_array.npy' 
    base = np.load(f'{os.getcwd()}\\{arr_path}', allow_pickle=True)

    return base

