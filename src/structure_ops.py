import numpy as np
from helpers import structure_vlist

def mask_neighbours(vl, cv):
    mask = (vl != cv)
    return vl[mask]

def neighbours(vl): 
    n_list = [mask_neighbours(vl,vl[i]) for i in range(vl.size)]
    return np.array(n_list)
    
class StructOps: 
    def __init__(self, vlist): 
        
        self.vlist = structure_vlist(vlist)
        self.neighbours = neighbours(self.vlist)


    
    def avg_pos(self):
    
        avg_pos = np.sum(self.neighbours['position'], axis=1)
        avg_pos = avg_pos / self.neighbours.shape[1]
        dv = avg_pos - self.vlist['position']
        mag = np.linalg.norm(dv, axis=1)

        if not mag.any(): 
            return np.zeros(2)
        
        else: 
            dv /= mag[:,np.newaxis]
            return dv
        
    
    def alignment(self):
        vels = np.sum(self.neighbours['velocity'], axis=1) 
        vels /= self.neighbours.shape[1]

        v_mag = np.linalg.norm(vels, axis=1)
        
        if not v_mag.any():
            return np.zeros(2)

        else:
            normalized = np.divide(vels,v_mag[:,np.newaxis])
            return normalized

    def separate(self, desired_sep=100): 
        pass
        
        ''' original function: 
        1. get diffs 
        2. get magnitude
        3. if magnitude within 0 and desired separation (function parameter)
            4. normalize diff (diff / diff_mag)
            5. **divide normalized by mag again  
                    *scale norm so the closer an obstacle is, the higher the sf
                    
        '''
        
        
        diffs = np.subtract(self.vlist['position'][:,np.newaxis], self.neighbours['position'])
        # mags = np.linalg.norm(diffs, axis=1)
        mags = np.linalg.norm(diffs, axis=2)
        norm = diffs / mags[:,np.newaxis:,np.newaxis] 

        mask_mags = (mags > desired_sep)

        scaled_mags = mags[mask_mags]
        #scaled_mags = mags[mags > 100]

        scaled_mags = np.where(mags>desired_sep, 1, mags)

        norm = np.divide(norm,scaled_mags[:,np.newaxis:,np.newaxis])
        return np.sum(norm, axis=1)

        
        



