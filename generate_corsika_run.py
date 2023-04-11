from generate_run_layout import (create_layout, 
                          template, create_inputs, 
                          create_sbatch, create_launch,
                          create_input_params,
                          create_sbatch_params)
import subprocess


run_layout = create_layout("17_simple_run")


njobs = 1
nruns = 600
batch_files = []
for run_number in range(nruns):
    input_params = create_input_params(run_layout, run_number)
    inputs_file = create_inputs(run_layout, template, 
                                input_params, run_number)

    sbatch_params = create_sbatch_params(run_layout, inputs_file, 
                                         run_number, njobs)
    batch_file = create_sbatch(run_layout, template,
                            sbatch_params, run_number)
   
    batch_files.append(batch_file)   
    
launch_file = create_launch(run_layout, template, batch_files)

proc = subprocess.run([f"{launch_file}"], 
                   stdout=subprocess.PIPE, 
                   stderr=subprocess.PIPE)

print(f"stdout:\n{proc.stdout.decode()}")  
print(f"stderr:\n{proc.stderr.decode()}")