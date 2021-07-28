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
        # print(indices)
        return indices
        # self.nearby_vects = [self.neighbour_positions[i] for i in indices]
    
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

        return total