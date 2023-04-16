import numpy as np
from read_file import read_corsika_file, as_numpy_arrays
from process_data import final_values


class Corsika2Dict:
    def __init__(self, corsika_file, zenith_angle, maps):
        read_data = read_corsika_file(corsika_file)
        self.num_primaries = read_data[2]
        
        np_values = as_numpy_arrays(*read_data[:2])  
        (self.pdgs, 
         self.obs_levels, 
         self.angles, 
         self.kin_energy) = final_values(*np_values, zenith_angle, maps)
        
        
    def distr_dict(self, pdgs_to_get):
        
        obs_levels_range = np.unique(self.obs_levels)
        corsika_results_dict = {}

        for pdg in pdgs_to_get:
            corsika_results_dict[pdg] = {}
            for obslev_id in obs_levels_range:
                corsika_results_dict[pdg][obslev_id] = {'theta [rad]': [], 
                                                        'energy [GeV]': []}
            
                filtered_ids = np.where((self.pdgs == pdg) & (self.obs_levels == obslev_id))[0]
                corsika_results_dict[pdg][obslev_id]['theta [rad]'] = self.angles[filtered_ids]
                corsika_results_dict[pdg][obslev_id]['energy [GeV]'] = self.kin_energy[filtered_ids]  
        
        corsika_results_dict['num_primaries'] = np.int64(self.num_primaries)
        
        return corsika_results_dict