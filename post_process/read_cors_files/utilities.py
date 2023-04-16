import numpy as np
from particle import Corsika7ID, Particle


def pdg_mass_maps(max_id = 70):
    """Returns 2 numpy arrays which maps Corsika `ids` up to max_id
    (not included, i.e. [0,max_id-1], max_id = 70 by default)

    Args:
        max_id (int, optional): maximum id to map. Defaults to 70.

    Returns:
        `tuple(pdg_map, mass_map)`: 
        `pdg_map`: pdg_map[corsika_id] == pdg_id 
        (or minimum integer -2147483648 if no corsika_id exists, e.g.
        0 doesn't corresponds to any particle in Corsika)
        `mass_map`: mass_map[corsika_id] == mass (in GeV)
    """
    pdg_map = np.empty(max_id, dtype=np.int32)
    mass_map = np.empty(max_id, dtype=np.float32)

    min_int = np.iinfo(np.int32).min
    for i in range(pdg_map.size):
        try:
            pdg = int(Corsika7ID.to_pdgid(i))
        except Exception as ex:
            pdg = min_int
        
        try:
            mass = Particle.from_pdgid(pdg).mass/1e3
            if mass is None:
                mass = 0
        except Exception as ex:
            mass = 0
        
        pdg_map[i] = pdg
        mass_map[i] = mass
        
    return pdg_map, mass_map    


def angle_and_p2(px, py, pz, zenith_angle):
    """Returns angle between direction of initial particle
    and the particle described by px, py, pz.
    Initial direction is `n = (sin(theta), 0, cos(theta))`, where
    `theta = zenith_angle`
    As a byproduct returns also square of momentum 
    (`px**2 + py**2 + pz**2`) required for energy calculation 

    Args:
        px (np.array): array of `px` momentum
        py (np.array): array of `py` momentum
        pz (np.array): array of `pz` momentum
        zenith_angle (float): zenith angle in `degrees`
    Returns:
        tuple(angles, p2): angles in radian, p2 in (GeV/c)**2
    """
    # stack the three vectors into a 2D array
    p = np.stack((px, py, pz), axis=1)

    # compute p2 as the sum of squares of px, py, and pz
    p2 = np.sum(p**2, axis = 1)

    # compute the norm of each row of the array
    p_norm = np.sqrt(p2)

    # normalize the rows of the array to get the direction vectors
    ndir = p / p_norm[:, np.newaxis]
    
    ndir0 = np.array([np.sin(np.radians(zenith_angle)), 
                      0, 
                      np.cos(np.radians(zenith_angle))])
    
    # compute the angle between ndir and ndir0 in radians
    # clip insures, that cos slightly higher than 1 (1.00004)
    # will be replaced by 1
    cos_clip = np.clip(np.sum(ndir * ndir0, axis=1), a_min=-1.0, a_max=1.0)
    angles = np.arccos(cos_clip)    
    return angles, p2


def mass_pdg_level(particle_description):
    """Returns mass, pdg, and level arrays from 
    `particle_description` array returned by Corsika

    Args:
        particle_description (np.array): Corsika particle_description
    Returns:
        tuple(masses, pdgs, obs_levels): 
        `masses` in GeV
        `pdgs` pdg ids
        `obs_levels` ids of observation levels (starting from `0`)
    """
    pdg_map, mass_map = pdg_mass_maps(200)
    
    
    corsika_pids = np.array(particle_description // 1000, dtype=np.int32)
    obs_levels = np.array((particle_description % 10) - 1, dtype=np.int32)
    masses = mass_map[corsika_pids]
    pdgs = pdg_map[corsika_pids]
    return masses, pdgs, obs_levels
    

def kinetic_energy(mass, p2):
    return p2/(np.sqrt(p2 + mass**2) + mass)
    

def final_values(particle_description, px, py, pz, zenith_angle):
    """Return quantities: `pdgs, obs_levels, angles, kin_energy`
    obtained from Corsika data

    Args:
        particle_desc (np.array): Corsika description id
        px (np.array): in GeV
        py (np.array): in GeV
        pz (np.array): in GeV
        zenith_angle (np.array): in deg

    Returns:
        tuple(pdgs, obs_levels, angles, kin_energy): 
        `pdgs`: pdg ids
        `obs_levels`: id of observation angle (zero-based)
        `angles`: between intial direction in radian
        `kin_energy`: kinetic energy in (GeV)
    """
    
    masses, pdgs, obs_levels = mass_pdg_level(particle_description)
    angles, p2 = angle_and_p2(px, py, pz, zenith_angle)
    kin_energy = kinetic_energy(masses, p2)
    
    return pdgs, obs_levels, angles, kin_energy