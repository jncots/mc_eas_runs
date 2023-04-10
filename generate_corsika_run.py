from pathlib import Path
from generate_run_layout import (create_layout, 
                          template, create_inputs, create_sbatch)
import stat
import subprocess


run_layout = create_layout("08_simple_run")


run_number = 6
results_dir = str(run_layout["results_dir"]) 
input_params = {
    "run_number" : run_number,
    "num_showers" : 10,
    "prime_energy" : 100,
    "zenith_angle" : 30,
    "seed_1" : 100,
    "seed_2" : 200,
    "observ_level" : f"{3e5:E}", # 3 km
    "muon_mult_scat" : "F",
    "output_directory" : f"{results_dir}/"}


inputs_file = create_inputs(run_layout, template, 
                            input_params, run_number)

# sbatch script
sbatch_params = {"inputs_file" : inputs_file,
                 "logs_dir" : str(run_layout["logs_dir"]),
                 "job_name" : f"corsika_run{run_number}"}


batch_file = create_sbatch(run_layout, template,
                           sbatch_params, run_number)
    
batch_files = [batch_file]    
    
launch_file = run_layout["scripts_dir"]  / f"launch.sh" 
launch_params = {"scripts_dir" : run_layout["scripts_dir"] }

with open(template["launch"]) as ftemp:
    launch_template = ftemp.read().format(**launch_params)

for batch_file in batch_files:
    launch_template += f"\nsbatch {batch_file}"


with open(launch_file, "w") as f:
    f.write(launch_template)    
    
launch_file.chmod(launch_file.stat().st_mode | stat.S_IEXEC)

proc = subprocess.run([f"{launch_file}"], 
                   stdout=subprocess.PIPE, 
                   stderr=subprocess.PIPE)

print(f"stdout:\n{proc.stdout.decode()}")  
print(f"stderr:\n{proc.stderr.decode()}")