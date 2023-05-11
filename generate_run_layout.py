from pathlib import Path
import stat
import random
import math

python_script_dir = Path(__file__).parent

corsika_inputs_dir = "inputs_templates/spectrum_runs"
corsika_inputs_dir = python_script_dir / corsika_inputs_dir

corsika_inputs_template = "corsika_inputs_template_019"
corsika_sbatch_template = "corsika_sbatch_template"
corsika_launch_template = "launch_template"

corsika_inputs_template = corsika_inputs_dir / corsika_inputs_template
corsika_sbatch_template = python_script_dir / corsika_sbatch_template
corsika_launch_template = python_script_dir / corsika_launch_template

template = {
    "inputs": corsika_inputs_template,
    "sbatch": corsika_sbatch_template,
    "launch": corsika_launch_template,
}


def create_layout(run_name):
    base_dir = "/dicos_ui_home/antonpr/work/"
    dir_with_runs = "corsika_runs/spectrum_run"
    base_dir = Path(base_dir)
    dir_with_runs = base_dir / dir_with_runs

    run_directory = dir_with_runs / run_name
    scripts_dir = run_directory / "scripts"
    logs_dir = run_directory / "logs"
    results_dir = run_directory / "results"

    run_layout = {
        "scripts_dir": scripts_dir,
        "logs_dir": logs_dir,
        "results_dir": results_dir,
    }

    for directory in run_layout.values():
        directory.mkdir(parents=True, exist_ok=True)

    return run_layout


def create_inputs(run_layout, template, input_params, run_number):
    inputs_file = run_layout["scripts_dir"] / f"inputs_run_{run_number}"
    with open(template["inputs"]) as ftemp:
        with open(inputs_file, "w") as fout:
            fout.write(ftemp.read().format(**input_params))

    return inputs_file


def create_sbatch(run_layout, template, sbatch_params, run_number):
    batch_file = run_layout["scripts_dir"] / f"sbatch_run_{run_number}"
    with open(template["sbatch"]) as ftemp:
        with open(batch_file, "w") as fout:
            fout.write(ftemp.read().format(**sbatch_params))

    return batch_file


def create_launch(run_layout, template, batch_files):
    launch_file = run_layout["scripts_dir"] / f"launch.sh"
    launch_params = {"scripts_dir": run_layout["scripts_dir"]}

    with open(template["launch"]) as ftemp:
        launch_template = ftemp.read().format(**launch_params)

    for batch_file in batch_files:
        launch_template += f"\nsbatch {batch_file}"

    with open(launch_file, "w") as f:
        f.write(launch_template)

    launch_file.chmod(launch_file.stat().st_mode | stat.S_IEXEC)

    return launch_file


def convert_km2cm(observ_levels):
    lev_str = []
    for level in observ_levels:
        level = level * 1e5
        lev_str.append(f"{level:E}")
    return lev_str


def convert_X2cm(X_levels):
    """
    This is a conversion for specific case
    of homogeneous atmosphere where X = 1000 at surface
    """
    lev_str = []
    for X_level in X_levels:
        # 1e-5 shifts a little bit
        # so that X = 1000 -> 1e-5 cm (not exactly 0)
        # level = (1.00892857e3 - X_level) * 1.12e4
        # level = (3.00012930e+03 - X_level) * 7.73395205e+02
        # level = (1.45850400e+04 - X_level) * 7.77247586e+02
        level = -1.12e09 * math.log((X_level + 1.44087935e06) / 1.45546439e06)
        lev_str.append(f"{level:E}")
    return lev_str


def create_input_params(run_layout, run_number, num_showers=500):
    max_rnd_number = int(1e6)
    results_dir = str(run_layout["results_dir"])
    # obs_levels = convert_km2cm([0, 5, 15, 20]) # in km
    # 1.21917, 4.89638, 15.00823 equals to
    # 143, 647, 1033 g/cm2 for theta = 30 deg
    # obs_levels = convert_km2cm([0, 50, 90])
    # --- USStd 0 degree:
    # h=143, X=14.096117926440979 km
    # h=647, X=3.808506428696458 km
    # h=1033, X=0.025232939039804742 km
    # obs_levels = convert_km2cm([0.025232939039804742,
    #                             3.808506428696458,
    #                             14.096117926440979])
    obs_levels = convert_X2cm([1000, 5000, 10000])
    input_params = {
        "run_number": run_number,
        "num_showers": num_showers,
        # "prime_energy": 100 + 0.105658,  # in GeV
        "spectrum_slope": -3.0,
        "prime_energy1": 0.5,
        "prime_energy2": 1000,
        "primary_particle": 6,  # 6 is muon
        # "prime_energy" : 1e6 + .105658, # in GeV muon
        # "prime_energy" : 100 + 0.938272, # in GeV
        # "primary_particle" : 14, # 14 is proton
        "zenith_angle": 0,  # in degrees
        "seed_1": random.randrange(max_rnd_number),
        "seed_2": random.randrange(max_rnd_number),
        "observ_level1": obs_levels[0],
        "observ_level2": obs_levels[1],
        "observ_level3": obs_levels[2],
        "transition_energy": 200,  # in GeV
        "muon_mult_scat": "T",
        "output_directory": f"{results_dir}/",
    }

    return input_params


def create_sbatch_params(run_layout, inputs_file, run_number, njobs):
    sbatch_params = {
        "inputs_file": inputs_file,
        "logs_dir": str(run_layout["logs_dir"]),
        "job_name": f"corsika_run{run_number}",
        "njobs": njobs,
    }

    return sbatch_params
