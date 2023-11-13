from slurm_launcher import output_env, run_job

output_file, error_file, script_file = output_env(
    "/dicos_ui_home/antonpr/work/runs/ml/gpu_03"
)

slurm_directives = {
    "job-name": "test",
    "array": "1-1",
    "ntasks": 1,
    "mem": "3gb",
    "gpus": 1,
    "cpus-per-task": 1,
    "partition": "v100_short",
    "time": "00:02:00",
    "output": output_file,
    "error": error_file,
}

app_info = {
    "application": "date\nhostname\nnvidia-smi",
    "working_dir": "/dicos_ui_home/antonpr/ml/erdmann/airshower",
}


run_job(slurm_directives, app_info, script_file)
