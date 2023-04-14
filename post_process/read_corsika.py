from corsikaio import CorsikaParticleFile

for filename in tqdm(corsika_datafiles, total = len(corsika_datafiles)):
    try:
        # time.sleep(2)
        with CorsikaParticleFile(filename) as f:
            signal.alarm(0)    
            
            counter = 0
            for e in f:
                        
                particle_data = e.particles

                particles_in_subblock = particle_data['particle_description']
                pids_in_subblock = (particles_in_subblock - (particles_in_subblock % 1000)) / 1000
                
                for pdg in get_pdg:
                    
                    show_corsika_id = corsika_id_dict[pdg]
                    show_corsika_id_bar = corsika_id_dict[-pdg]
                    
                    part_mass = mass_dict_GeV[np.abs(pdg)]

                    filter_pid_inds = np.where((pids_in_subblock == show_corsika_id))[0]

                    filtered_obslevels = np.array(particles_in_subblock % 10)[filter_pid_inds] 
                    
                    filtered_pz = particle_data['pz'][filter_pid_inds]
                    filtered_px = particle_data['px'][filter_pid_inds]
                    filtered_py = particle_data['py'][filter_pid_inds]
                    
                    filtered_x = particle_data['x'][filter_pid_inds]
                    filtered_y = particle_data['y'][filter_pid_inds]
                    
                    filtered_unique_ids = particles_in_subblock[filter_pid_inds]
                    
                    
                    r = np.sqrt(filtered_x**2 + filtered_y**2)
                    

                    filtered_pT = np.sqrt(filtered_px**2 + filtered_py**2)
                    
                    filtered_ptot = np.sqrt(filtered_px**2 + filtered_py**2 + filtered_pz**2)
                

                    filtered_theta = np.arctan2(filtered_pT, filtered_pz)
                    filtered_phi = np.arctan2(filtered_py, filtered_px)
                    
                    init_dir = np.array([np.ones_like(filtered_phi) * np.sin(np.radians(theta)), 
                            np.zeros_like(filtered_phi) * np.sin(np.radians(theta)),
                            np.ones_like(filtered_phi) * np.cos(np.radians(theta))]).T
                    
                    final_dir = np.array([np.cos(filtered_phi) * np.sin(filtered_theta),
                                        np.sin(filtered_phi) * np.sin(filtered_theta),
                                        np.cos(filtered_theta)]).T
                    
                    dot_products = np.arccos(np.sum(init_dir * final_dir, axis=1))
                    
                    filtered_energies = np.sqrt(filtered_pT**2 + filtered_pz**2 + part_mass**2) - part_mass

                    for obslev_id in level_range:

                        this_obslev_inds = np.where(filtered_obslevels == obslev_id)[0]

                        all_thetas_corsika[pdg][obslev_id].extend(dot_products[this_obslev_inds])

                        all_energies_corsika[pdg][obslev_id].extend(filtered_energies[this_obslev_inds])
                        
                        all_unique_pids[pdg][obslev_id].extend(filtered_unique_ids[this_obslev_inds])
    except Exception as ex: 
        print(ex)
        print(filename.name)
        continue                        