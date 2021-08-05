
def generate():
    import numpy as np
    from helpers import genlist
    
    fn = r'C:\Users\Sanjay\code\projects\boids_2.0\tests\test_env\Tests\static_vl.npy'
    vl = genlist(100)

    np.save(fn,vl)

