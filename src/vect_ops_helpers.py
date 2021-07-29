import numpy as np 

class VectOps(): 
    def __init__(self, vlist): 
        self.vlist = vlist
        for cv in vlist: 
            cv.nearby_vects = [v for v in vlist if v != cv]

    def avg_pos(self): 
        avg_list = [] 
    
        for v in self.vlist: 
            avg_list.append(v.avg_position())

        return np.array(avg_list)

    def non_norm_avg(self): 
        avg_list = [] 
    
        for v in self.vlist: 
            s = sum([nv.position for nv in v.nearby_vects])
            s /= len(v.nearby_vects)

            avg_list.append(s)
        return np.array(avg_list)

    def dv_test(self): 
        avg_list = [] 
        mags = [] 
    
        for v in self.vlist: 
            s = sum([nv.position for nv in v.nearby_vects])
            s /= len(v.nearby_vects)

            dv = s - v.position

            avg_list.append(dv)
            mags.append(np.linalg.norm(dv))
        return np.array(avg_list), np.array(mags)

    def sum_position(self): 

        sums = [] 
        for v in self.vlist: 
            sums.append(sum([nv.position for nv in v.nearby_vects]))

        return np.array(sums)

    def align(self): 
        alignment = [] 

        for v in self.vlist:
            alignment.append(v.alignment())

        return np.array(alignment)

    def sep(self, desired_sep = 100): 
        separation = [] 

        for v in self.vlist:
            separation.append(v.separate(desired_sep))

        return np.array(separation)
        # return np.array([v.separate() for v in self.vlist])

    def diffs(self): 
        d = []

        return d

