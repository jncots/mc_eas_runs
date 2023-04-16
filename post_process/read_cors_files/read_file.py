import numpy as np
from corsikaio import CorsikaParticleFile


def read_corsika_file(corsika_file):
    results = []
    tot_size = 0
    num_primaries = 0
    with CorsikaParticleFile(corsika_file) as f:
            for e in f:
                results.append(e.particles)
                tot_size += results[-1].size
                num_primaries += 1
                
    return tot_size, results, num_primaries            


def as_numpy_arrays(tot_size, corsika_data):
    """Join all blocks of data in `results` 
    (structured arrays) as a single array for
    a specific quantity

    Args:
        tot_size (int): total number of particles
        results (list of structured arrays): 
        structured arrays from a corsika file

    Returns:
        tuple of numpy arrays: quanities
    """
    particle_desc = np.empty(tot_size, dtype=np.float32)
    particle_px = np.empty(tot_size, dtype=np.float32)
    particle_py = np.empty(tot_size, dtype=np.float32)
    particle_pz = np.empty(tot_size, dtype=np.float32)
    # particle_x = np.empty(tot_size, dtype=np.float32)
    # particle_y = np.empty(tot_size, dtype=np.float32)
    # particle_t = np.empty(tot_size, dtype=np.float32)
    
    prev_ind = 0
    for result in corsika_data:
        next_ind = prev_ind + len(result)
        particle_desc[prev_ind:next_ind] = result["particle_description"]
        particle_px[prev_ind:next_ind] = result["px"]
        particle_py[prev_ind:next_ind] = result["py"]
        particle_pz[prev_ind:next_ind] = result["pz"]
        # particle_x[prev_ind:next_ind] = result["x"]
        # particle_y[prev_ind:next_ind] = result["y"]
        # particle_t[prev_ind:next_ind] = result["t"]
        prev_ind = next_ind
        
    return particle_desc, particle_px, particle_py, particle_pz
