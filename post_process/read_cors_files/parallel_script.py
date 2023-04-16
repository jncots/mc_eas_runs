import multiprocessing
from tqdm import tqdm

from find_files import corsika_data_files
from process_data import pdg_mass_maps
from corsika2dict import Corsika2Dict, join_dicts
from save2hdf5 import save_dict_to_hdf5


       
def dict_for_hdf5(file):
    pdgs_to_get = [-12, 12, -13, 13, -14, 14]
    theta = 30
    maps = pdg_mass_maps()
    
    corsika_dict = Corsika2Dict(file, theta, maps)
    return corsika_dict.distr_dict(pdgs_to_get)



if __name__ == '__main__':
    import time
    data_files = corsika_data_files("34_simple_run")
    
    start = time.time()
    results = []
    with multiprocessing.Pool() as pool:
        for result in tqdm(pool.imap_unordered(dict_for_hdf5, data_files), 
                           total=len(data_files)):
            results.append(result)
    
        
    save_dict_to_hdf5(join_dicts(results), 
                    data_files[0].parents[1]/"corsika_ang_en.hdf5")
    end = time.time()
    print(f"Elapsed time = {end - start}")