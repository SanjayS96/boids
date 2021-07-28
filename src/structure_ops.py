import numpy as np


def avg_pos(vl,neighbours=None):
    
    avg_pos = np.sum(neighbours['position'], axis=1)
    avg_pos = avg_pos / neighbours.shape[1]
    dv = avg_pos - vl['position']
    mag = np.linalg.norm(dv, axis=1)

    if not mag.any(): 
        return np.zeros(2)
    
    else: 
        dv /= mag[:,np.newaxis]
        return dv

def alignment(neighbours_list):
    vels = np.sum(neighbours_list['velocity'], axis=1) 
    vels /= neighbours_list.shape[1]

    v_mag = np.linalg.norm(vels, axis=1)
    
    if not v_mag.any():
        return np.zeros(2)

    normalized = np.divide(vels,v_mag[:,np.newaxis])
    return normalized
    
def separation(vl, neighbours_list): 
    diffs = vl['position'] - neighbours_list['position']
    return diffs



def mask_neighbours(vl, cv):
    mask = (vl != cv)
    return vl[mask]

def mask_neighbours2(vl, cv):
    mask = (vl != cv)
    return vl[mask]

def vectorize_neighbours(vl): 
    v = np.vectorize(mask_neighbours2, otypes=[object], signature='(n),()->()')
    return v(vl,vl)


def neighbours(vl): 
    n_list = [mask_neighbours(vl,vl[i]) for i in range(vl.size)]
    return np.array(n_list)

def neighbours2(vl): 
    n_list = [] 
    v_list = []
    for i in range(vl.size): 
        cv = vl[i]
        n_list.append(mask_neighbours(vl, cv))
        v_list.append(cv)
    
    return np.array(n_list), np.array(v_list)

    