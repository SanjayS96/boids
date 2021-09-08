import numpy as np
import numpy.ma as ma

from helpers import structure_vlist
from scipy.spatial import KDTree

def mask_neighbours(vl, cv):
    mask = (vl != cv)
    return vl[mask]

def neighbours(vl): 
    n_list = [mask_neighbours(vl,vl[i]) for i in range(vl.size)]
    return np.array(n_list)
    
class StructOps: 
    # def __init__(self, vlist=None): 
        
    #     self.vlist = vlist
    #     if vlist is not None:
    #         self.vlist = structure_vlist(vlist)

    #     self.neighbours = neighbours(self.vlist)
    #     self.maxspeed = vlist[0].maxspeed

    def __init__(self, num): 
        
        self.vlist = structure_vlist(num)

        self.neighbours = neighbours(self.vlist)
        self.neighbour_distance = 50
        self.maxspeed = 6

    def recheck_neighbours(self): 
        
        '''will have to benchmark diag vs eye:
        diag = np.diag(a.vlist)
        d = a.vlist!=diag
        n = vlist_matrix[d]
        '''
        vlist_matrix =np.vstack([self.vlist for i in range(self.vlist.shape[0])])
        eye = np.eye(self.vlist.shape[0], dtype=bool)
        invert_eye = ~eye
        flat_neighbours = vlist_matrix[invert_eye]
        self.neighbours = flat_neighbours.reshape(self.vlist.shape[0], self.vlist.shape[0]-1)


    def scipy_neighbours(self): 
        tree = KDTree(self.vlist['position'])
        vlist_matrix =np.vstack([self.vlist['position'] for i in range(self.vlist.shape[0])])
        mags, indices = tree.query(vlist_matrix, 5)

        return indices

    def initialize_vlist():
        pass
    
    def nearby_neighbours(self): 
        vlist_matrix =np.vstack([self.vlist for i in range(self.vlist.shape[0])])

        diffs = self.vlist['position'][:,np.newaxis] - vlist_matrix['position']
        mags = self.alt_mag(diffs)
        mask = (mags < self.neighbour_distance) & (mags!=0)
        ma_mask = ma.masked_where(~mask, vlist_matrix)
        self.neighbours = ma_mask
        return mask
    


        


    def mag(self, dv, axis): 
        return np.linalg.norm(dv, axis=axis)

    def alt_mag(self, dv):
        return np.sqrt(np.einsum('ijk,ijk->ij', dv, dv))
    
    def alt_mag_axis1(self, dv):
        return np.sqrt(np.einsum('ij,ij->i', dv, dv))

    def avg_pos(self):
        
        
        avg_pos = np.sum(self.neighbours['position'], axis=1)
        if self.neighbours.shape[1] == 0: 
            return np.zeros(2)
        
        avg_pos = avg_pos / self.neighbours.shape[1]

        dv = avg_pos - self.vlist['position']
        mag = self.mag(dv, axis=1)

        mask = mag>0
        dv[mask] /= mag[mask][:,np.newaxis]

        return dv
    
    def avg_pos_masked(self): 
        dv = np.zeros(2)
        avg_pos = self.neighbours['position'].mean(axis=1).data
        
        if avg_pos.any():
            dv = avg_pos - self.vlist['position']
            mag = self.alt_mag_axis1(dv)

        
            dv/= mag[:,np.newaxis]

        return dv

    def steer_to_mouse(self, target): 
        diff = target - self.vlist['position']
        mag = self.mag(diff, axis=1)
        
        norm = diff/mag[:,np.newaxis]
        
        return norm
        
    def limit_speed(self, maxspeed): 
        
        speed_mag = np.linalg.norm(self.vlist['velocity'], axis=1)
        speed_mask = (speed_mag > maxspeed)
        
        # self.vlist['velocity'][speed_mask] = self.maxspeed[:,np.newaxis]
        over_limit = self.vlist['velocity'][speed_mask]
        if over_limit.any():
            
            mag = np.linalg.norm(over_limit, axis=1)
            # self.vlist[speed_mask] = (over_limit/mag[:,np.newaxis]) * self.maxspeed  
            over_limit /= mag[:,np.newaxis]
            over_limit *= maxspeed

            self.vlist['velocity'][speed_mask] = over_limit



        
        
        


    def alignment(self):
        vels = np.sum(self.neighbours['velocity'], axis=1) 
        vels /= self.neighbours.shape[1]

        v_mag = self.mag(vels, axis=1)
        
        if not v_mag.any():
            return np.zeros(2)

        else:
            normalized = np.divide(vels,v_mag[:,np.newaxis])
            return normalized
    def alignment_masked(self): 
        vels = np.sum(self.neighbours['velocity'], axis=1) 
        # vels = np.where(not vels.any(), vels, np.zeros(2))
        vels /= ma.count_masked(self.neighbours['velocity'], axis=1)

        v_mag = self.mag(vels, axis=1)
        
        normalized = np.divide(vels, v_mag[:,np.newaxis])
        return normalized
    def basic_sep(self, desired_sep): 
        diffs = np.subtract(self.vlist['position'][:,np.newaxis], self.neighbours['position'])
        mags = self.alt_mag(diffs)
        mask = ((mags<desired_sep) & (mags > 0))

        diffs[mask] /= mags[mask][:,np.newaxis]

        summed = diffs[mask].sum(axis=1)
        
        dv = summed / np.count_nonzero(diffs[mask])
        return dv[:,np.newaxis]
        # return np.sum(diffs[mask], axis=1)

        summed = np.sum(norm, axis=1)
        count = np.count_nonzero(norm, axis=1)

        return summed/count



    def separate(self, desired_sep=40, debug=False): 
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
        scaled = np.divide(norm,sel_mags[:,np.newaxis:,np.newaxis])
        

        total = np.sum(scaled, axis=1)
        total_count = np.count_nonzero(mags_mask, axis=1)
        
        total_count = np.where(total_count!=0, total_count, np.ones(1))
        
        '''instead of replacing zeros with ones to avoid zero div error, 
        should use similar method as normalized total to only divide nonzero vals

        "avg_total = np.divide(total, total_count, out=np.zeros_like(total), where=total_count>0)"
        not working, due to shape mismatch. probably have to add an axis to total_count '''
        
        avg_total = total / total_count[:,np.newaxis]
        total_mag = self.mag(avg_total, axis=1)

        normalized_total = np.divide(avg_total,total_mag[:,np.newaxis], out=np.zeros_like(avg_total), where=total_mag[:,np.newaxis]!=0)

        if not debug:
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

    def separate_bench_dict(self, desired_sep=40): 
        
        '''
        possible improvements:
            1. replace np.linalg.norm:
                -np.sqrt(m.dot(m))   
                -np.sqrt(m*m))
                -np.sqrt(np.einsum('i,i', a, a))
                -np.sqrt(inner1d(V,V))

            2. use mag^2 for mags mask against desired_sep^2
        '''

        import time

        timings = {}

        total = np.zeros(2) #placeholder
        
        start_time=time.perf_counter()
        
        diffs = np.subtract(self.vlist['position'][:,np.newaxis], self.neighbours['position'])
        
        last_time = time.perf_counter() 
        timings['diffs'] = last_time - start_time  

        last_time = time.perf_counter() 
        mags = self.mag(diffs, axis=2)
        timings['mags'] = time.perf_counter() - last_time
        # timings['mags_perf'] = time.perf_counter()

        last_time = time.perf_counter()
        mags_mask = ((mags<desired_sep) & (mags > 0))
        timings['mags_mask'] = time.perf_counter() - last_time
        
        
        last_time = time.perf_counter()
        sel_mags = np.where(mags_mask, mags, np.ones(1))
        timings['sel_mags'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        sel_diffs = np.where(mags_mask[:,np.newaxis:,np.newaxis], diffs, np.zeros(2))
        timings['sel_diffs'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        norm = sel_diffs / sel_mags[:,np.newaxis:,np.newaxis]
        timings['norms'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        scaled = np.divide(norm,sel_mags[:,np.newaxis:,np.newaxis])
        timings['scaled'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        total = np.sum(scaled, axis=1)
        timings['sum_scaled'] = time.perf_counter() - last_time

        last_time = time.perf_counter()
        total_count = np.count_nonzero(mags_mask, axis=1)
        last_time = time.perf_counter()
        timings['count_nonzero'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        total_count = np.where(total_count!=0, total_count, np.ones(1))
        timings['total_count'] = time.perf_counter() - last_time
        
        '''instead of replacing zeros with ones to avoid zero div error, 
        should use similar method as normalized total to only divide nonzero vals

        "avg_total = np.divide(total, total_count, out=np.zeros_like(total), where=total_count>0)"
        not working, due to shape mismatch. probably have to add an axis to total_count '''
        
        last_time = time.perf_counter()
        avg_total = total / total_count[:,np.newaxis]
        timings['avg_total'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        total_mag = np.linalg.norm(avg_total, axis=1)
        timings['total_mag'] = time.perf_counter() - last_time

        last_time = time.perf_counter()
        normalized_total = np.divide(avg_total,total_mag[:,np.newaxis], out=np.zeros_like(avg_total), where=total_mag[:,np.newaxis]!=0)
        timings['normalized'] = time.perf_counter() - last_time

        timings['total'] = time.perf_counter()- start_time

        return timings
        return normalized_total

    def faster_bench_dict(self, desired_sep=40): 
        
        '''
        possible improvements:
            1. replace np.linalg.norm:
                -np.sqrt(m.dot(m))   
                -np.sqrt(m*m))
                -np.sqrt(np.einsum('i,i', a, a))
                -np.sqrt(inner1d(V,V))

            2. use mag^2 for mags mask against desired_sep^2
        '''

        import time

        timings = {}

        total = np.zeros(2) #placeholder
        
        start_time=time.perf_counter()
        
        diffs = np.subtract(self.vlist['position'][:,np.newaxis], self.neighbours['position'])
        
        last_time = time.perf_counter() 
        timings['diffs'] = last_time - start_time  

        last_time = time.perf_counter() 
        # mags = np.linalg.norm(diffs, axis=2)
        mags = self.alt_mag(diffs)
        timings['mags'] = time.perf_counter() - last_time
        # timings['mags_perf'] = time.perf_counter()

        last_time = time.perf_counter()
        mags_mask = ((mags<desired_sep) & (mags > 0))
        timings['mags_mask'] = time.perf_counter() - last_time
        
        
        last_time = time.perf_counter()
        sel_mags = np.where(mags_mask, mags, np.ones(1))
        timings['sel_mags'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        sel_diffs = np.where(mags_mask[:,np.newaxis:,np.newaxis], diffs, np.zeros(2))
        timings['sel_diffs'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        norm = sel_diffs / sel_mags[:,np.newaxis:,np.newaxis]
        timings['norms'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        scaled = np.divide(norm,sel_mags[:,np.newaxis:,np.newaxis])
        timings['scaled'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        total = np.sum(scaled, axis=1)
        timings['sum_scaled'] = time.perf_counter() - last_time

        last_time = time.perf_counter()
        total_count = np.count_nonzero(mags_mask, axis=1)
        last_time = time.perf_counter()
        timings['count_nonzero'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        total_count = np.where(total_count!=0, total_count, np.ones(1))
        timings['total_count'] = time.perf_counter() - last_time
        
        '''instead of replacing zeros with ones to avoid zero div error, 
        should use similar method as normalized total to only divide nonzero vals

        "avg_total = np.divide(total, total_count, out=np.zeros_like(total), where=total_count>0)"
        not working, due to shape mismatch. probably have to add an axis to total_count '''
        
        last_time = time.perf_counter()
        avg_total = total / total_count[:,np.newaxis]
        timings['avg_total'] = time.perf_counter() - last_time
        
        last_time = time.perf_counter()
        total_mag = self.alt_mag_axis1(avg_total)
        timings['total_mag'] = time.perf_counter() - last_time

        last_time = time.perf_counter()
        normalized_total = np.divide(avg_total,total_mag[:,np.newaxis], out=np.zeros_like(avg_total), where=total_mag[:,np.newaxis]!=0)
        timings['normalized'] = time.perf_counter() - last_time

        timings['total'] = time.perf_counter()- start_time

        return timings

    def faster_separate(self, desired_sep=40): 
        def diff(): 
            return np.subtract(self.vlist['position'][:,np.newaxis], self.neighbours['position'])

        diffs = diff()
        
        return diffs

    def debug_average(self): 
        avg_pos = np.sum(self.neighbours['position'], axis=1)
        if self.neighbours.shape[1] == 0: 
            return zeros
        
        avg_pos = avg_pos / self.neighbours.shape[1]
        # print(self.neighbours.shape)
        return avg_pos
    def steer_to_dv(self, dv, limit=0.2): 
        maxed = dv * 2
        steer_force = maxed - self.vlist['velocity'] 

        sf_mag = np.linalg.norm(steer_force, axis=1)
        sf_mag_zmask = (sf_mag==0)

        sf_mag[sf_mag_zmask] = 1
        steer_force = np.where(sf_mag[:,np.newaxis] > np.array(limit), (steer_force / sf_mag[:,np.newaxis]) * limit, steer_force)

        self.vlist['velocity'] += steer_force

        return self.vlist['velocity']
    def steer_debug(self, dv, limit=0.2): 
        maxed = dv * self.maxspeed
        steer_force = maxed - self.vlist['velocity'] 

        sf_mag = np.linalg.norm(steer_force, axis=1)
        zmask = (sf_mag!=0) & (sf_mag>limit)

        steer_force[zmask] /=sf_mag[zmask][:,np.newaxis]
        steer_force[zmask] *= limit




        return steer_force

        
        # steer_force = np.where(sf_mag[:,np.newaxis] > np.array(limit), (steer_force / sf_mag[:,np.newaxis]) * limit, steer_force)

        return steer_force

    def rotate(self): 
        rotations = np.arctan2(self.vlist['velocity'].T[0], self.vlist['velocity'].T[1])
        return rotations

    def screen_wrap(self, window_dimension): 
        breakpoint

        a = self.vlist['position'].copy()

        # where = np.where(self.vlist['position'] > )
        width,height = window_dimension
        x_axis = self.vlist['position'][:,0]        
        y_axis = self.vlist['position'][:,1]    

        x_axis[x_axis>width] = 0
        x_axis[x_axis< 0] = width

        y_axis[y_axis >height] = 0
        y_axis[y_axis< 0] =height

        # print(self.vlist['position'][0])

        # print(np.allclose(self.vlist['position'], a))
        # self.vlist['position'] = self.vlist['position'].reshape(2, self.vlist.shape[0])
        # over_mask = self.vlist['position'] > window_dimension
        # under_mask = self.vlist['position'] < window_dimension


        # self.vlist['position'][over_mask] -= window_dimension
        # self.vlist['position'][over_mask] -= window_dimension
        # self.vlist['position'][under_mask] += window_dimension


    def standard_neighbours(self, perception_radius=100): 
        diffs = self.vlist['position'][:,np.newaxis] - self.neighbours['position']
        mag = self.mag(diffs, axis=2)

        mag_mask = (mag < perception_radius)
        breakpoint
        return mag_mask
        # self.neighbours[mag_mask]

breakpoint