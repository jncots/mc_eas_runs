import numpy as np
from read_file import read_corsika_file, as_numpy_arrays
from process_data import final_values


class Corsika2Dict:
    def __init__(self, corsika_file, zenith_angle, maps):
        read_data = read_corsika_file(corsika_file)

        self.num_primaries = read_data[2]

        np_values = as_numpy_arrays(*read_data[:2])
        (self.pdgs, self.obs_levels, self.angles, self.kin_energy) = final_values(
            *np_values, zenith_angle, maps
        )

    def distr_dict(self, pdgs_to_get = None):
        obs_levels_range = np.unique(self.obs_levels)
        if pdgs_to_get is None:
            pdgs_to_get = np.unique(self.pdgs)
        
        corsika_results_dict = {}

        for pdg in pdgs_to_get:
            corsika_results_dict[pdg] = {}
            for obslev_id in obs_levels_range:
                corsika_results_dict[pdg][obslev_id] = {
                    "theta [rad]": [],
                    "energy [GeV]": [],
                }

                filtered_ids = np.where(
                    (self.pdgs == pdg) & (self.obs_levels == obslev_id)
                )[0]
                corsika_results_dict[pdg][obslev_id]["theta [rad]"] = self.angles[
                    filtered_ids
                ]
                corsika_results_dict[pdg][obslev_id]["energy [GeV]"] = self.kin_energy[
                    filtered_ids
                ]

        corsika_results_dict["num_primaries"] = np.int64(self.num_primaries)

        return corsika_results_dict


def join_dicts(results):
    corsika_results_dict = {}

    # Assume that all dicts have the same number of observation levels:
    result0 = results[0]
    pdgs_to_get = list(result0.keys())[:-1]
    obs_level_num = len(result0[pdgs_to_get[0]])
    
    pdgs_to_get = []
    obs_level_list = []
    for res in results:
        pdgs_in_res = list(res.keys())[:-1]
        pdgs_to_get += pdgs_in_res
        for pdg in pdgs_in_res:
            obs_level_list += res[pdg]
            
    
    obs_level_list = np.unique(obs_level_list)    
    pdgs_to_get = np.unique(pdgs_to_get)

    for pdg in pdgs_to_get:
        corsika_results_dict[pdg] = {}
        for obslev_id in obs_level_list:
            corsika_results_dict[pdg][obslev_id] = {"theta [rad]": [], "energy [GeV]": []}
            angles = []
            energies = []
            for res in results:
                if not res:
                    continue
                
                try:
                    angles.append(res[pdg][obslev_id]["theta [rad]"])
                    energies.append(res[pdg][obslev_id]["energy [GeV]"])
                except:
                    continue

            corsika_results_dict[pdg][obslev_id]["theta [rad]"] = np.concatenate(angles)
            corsika_results_dict[pdg][obslev_id]["energy [GeV]"] = np.concatenate(
                energies
            )

    num_primaries = 0
    for res in results:
        if not res:
            continue
        num_primaries += res["num_primaries"]

    corsika_results_dict["num_primaries"] = np.int64(num_primaries)

    return corsika_results_dict
