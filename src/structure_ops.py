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
        self.maxspeed = vlist[0].maxspeed

    
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

    def separate(self, desired_sep=40): 
        pass
        
        ''' original function: 
        1. get diffs 
        2. get magnitude
        3. if magnitude within 0 and desired separation (function parameter)
            4. normalize diff (diff / diff_mag)
            5. **divide normalized by mag again  
                    *scale norm so the closer an obstacle is, the higher the sf
                    
        '''
        
        total = np.zeros(2) #placeholder
        diffs = np.subtract(self.vlist['position'][:,np.newaxis], self.neighbours['position'])
        
        mags = np.linalg.norm(diffs, axis=2)
        mags_mask = ((mags<desired_sep) & (mags > 0))
        
        
        sel_mags = np.where(mags_mask, mags, np.ones(1))
        sel_diffs = np.where(mags_mask[:,np.newaxis:,np.newaxis], diffs, np.zeros(2))
        
        norm = sel_diffs / sel_mags[:,np.newaxis:,np.newaxis]
        scaled = np.divide(norm,mags[:,np.newaxis:,np.newaxis])
        

        total = np.sum(scaled, axis=1)
        total_count = np.count_nonzero(mags_mask, axis=1)
        
        total_count = np.where(total_count!=0, total_count, np.ones(1))
        
        '''instead of replacing zeros with ones to avoid zero div error, 
        should use similar method as normalized total to only divide nonzero vals

        "avg_total = np.divide(total, total_count, out=np.zeros_like(total), where=total_count>0)"
        not working, due to shape mismatch. probably have to add an axis to total_count '''
        
        avg_total = total / total_count[:,np.newaxis]
        total_mag = np.linalg.norm(avg_total, axis=1)

        normalized_total = np.divide(avg_total,total_mag[:,np.newaxis], out=np.zeros_like(avg_total), where=total_mag[:,np.newaxis]!=0)

        return normalized_total

        '''vscode unable to follow call stack when debugger invoked from venv.
        should configure remote debugging on laptop.
        can use a dict for inspecting values, in the mean time.'''   
           
        measures = {
            'diffs': diffs, 
            'diff_mags': mags, 
            'sel_mags': sel_mags,
            'norms': norm, 
            'scaled': scaled,

            'undiv_total': total, 
            'total_count': total_count,
            'avg_total': avg_total, 
            'total_mag': total_mag, 

            'totals': normalized_total
        
        }
        
        return measures

    def steer_to_dv(self, dv, limit=0.2): 
        maxed = dv * self.maxspeed
        steer_force = maxed - self.vlist['velocity'] 

        sf_mag = np.linalg.norm(steer_force, axis=1)
        steer_force = np.where(sf_mag[:,np.newaxis] > np.array(limit), (steer_force / sf_mag[:,np.newaxis]) * limit, steer_force)

        self.vlist['velocity'] += steer_force

        return self.vlist['velocity']
    def steer_debug(self, dv, limit=0.2): 
        maxed = dv * self.maxspeed
        steer_force = maxed - self.vlist['velocity'] 

        sf_mag = np.linalg.norm(steer_force, axis=1)
        steer_force = np.where(sf_mag[:,np.newaxis] > np.array(limit), (steer_force / sf_mag[:,np.newaxis]) * limit, steer_force)

        return steer_force

    def rotate(self): 
        pass

    def limit_speed(self): 
        pass




