import numpy as np
class Vector(): 
    def __init__(self, maxspeed=6): 
        rng = np.random.default_rng()
        
        self.position = rng.uniform(0,900,2)
        self.maxspeed = maxspeed
        
        rng = np.random.default_rng()
        rv = rng.uniform(-self.maxspeed, self.maxspeed, 2)

        self.velocity = rv
        self.acc = np.zeros(2)
        self.nearby_vects = [] 

    def avg_position(self):
        avg_pos = np.zeros(2)
        count = 0 

        if len(self.nearby_vects):
            for vect in self.nearby_vects: 
                if vect != self: 
                    avg_pos = np.add(avg_pos, vect.position)  
                    count +=1

            if count: 
                avg_pos = np.divide(avg_pos, count)
                dv = np.subtract(avg_pos, self.position)
                
            
                dv_mag = np.linalg.norm(dv)
                avg = np.divide(dv, dv_mag) #normalized 

                return avg

    def rotate(self): 
        self.rotation = np.arctan2(self.velocity[1], self.velocity[0])
    
    def scipy_tree(self, num_neighbours=5, positions=None): 
        
        tree = spatial.KDTree(positions)
        a, indices= tree.query(self.position, num_neighbours)
        return indices
    
    def alignment(self): 
        
        alignment = np.zeros(2)
        if len(self.nearby_vects) == 0: 
            return alignment

        for vect in self.nearby_vects: 
            if vect != self: 
                alignment += vect.velocity
        
        avg_alignment = alignment / (len(self.nearby_vects))
        al_mag = np.linalg.norm(avg_alignment)

        if al_mag > 0: 
            avg_alignment /= al_mag
        
        else: 
            avg_alignment = np.zeros(2)
        return avg_alignment

    def separate(self, desired_separation = 40): 
        
        total = np.zeros(2)
        count = 0 

        if len(self.nearby_vects):

            for vect in self.nearby_vects: 
                if vect != self:
                    diff = np.subtract(self.position, vect.position)
                    diff_mag = np.linalg.norm(diff)

                    if 0 < diff_mag < desired_separation: 
                        diff = np.divide(diff, diff_mag) #normalized distance from neighbour
                        scaled = np.divide(diff, diff_mag)
                        total = np.add(total, scaled)
                        count +=1
            
            if count > 0: 
                total = np.divide(total, count)
                total_mag = np.linalg.norm(total)    
                total = np.divide(total, total_mag)
        
        return total
    
    def separate_debug(self, desired_separation = 100): 
        
        undivided_total = np.zeros(2)
        total = np.zeros(2)
        total_mag = np.zeros(2)
        normalized_total = np.zeros(2)
        count = 0 

        
        diffs = [] 
        diff_mags = [] 
        norms = [] 
        over_mag = [] 
        scaled_list = [] 

        undivided_totals = [] 
        counts = [] 
        totals = [] 
        total_mags = [] 
        norm_totals = [] 

        for vect in self.nearby_vects: 
            if vect != self:
                diff = np.subtract(self.position, vect.position)
                diffs.append(diff)
                diff_mag = np.linalg.norm(diff)
                diff_mags.append(diff_mag)
                
                scaled = np.zeros(2)
                norm = np.zeros(2)
                
                if 0 < diff_mag < desired_separation: 
                    norm = np.divide(diff, diff_mag) #normalized distance from neighbour
                    scaled = np.divide(norm, diff_mag)
                    total = np.add(total, scaled)
                    count +=1

                norms.append(norm)
                scaled_list.append(scaled)
                
        undivided_totals.append(total.copy())
        counts.append(count)
        if count > 0: 
            total = np.divide(total, count)
            total_mag = np.linalg.norm(total)    
            normalized_total = np.divide(total, total_mag)
                
        totals.append(total)
        total_mags.append(total_mag)
        norm_totals.append(normalized_total)
        
        debug_dict = {
            'diffs': np.array(diffs), 
            'diff_mags': np.array(diff_mags), 
            'norms': np.array(norms), 
            'scaled': np.array(scaled_list),
            'undiv_totals': np.array(undivided_totals), 
            'counts': np.array(counts), 
            'total_mags': np.array(total_mags), 
            'norm_totals': np.array(norm_totals),
            'totals': np.array(totals)
        }
        return debug_dict

    def steer_to_dv(self, dv, limit=0.2): 
        dv = np.multiply(dv, self.maxspeed)
        steer_force = np.subtract(dv, self.velocity)
        
        sf_mag = np.linalg.norm(steer_force)

        if sf_mag > limit: 

            steer_force /= sf_mag
            steer_force *= limit

        self.acc += steer_force
        self.velocity += self.acc
        self.acc = np.zeros(2)

    def steer_force(self, dv, limit=0.2): 
        dv = np.multiply(dv, self.maxspeed)
        steer_force = np.subtract(dv, self.velocity)
        
        sf_mag = np.linalg.norm(steer_force)

        if sf_mag > limit: 

            steer_force /= sf_mag
            steer_force *= limit