from slurm_launcher import output_env, run_job

output_file, error_file, script_file = output_env(
    "/dicos_ui_home/antonpr/work/runs/ml/erdmann_10"
)

slurm_directives = {
    "job-name": "test",
    "array": "0-9",
    "ntasks": 1,
    "mem": "3gb",
    "cpus-per-task": 1,
    "partition": "short_serial",
    "time": "01:00:00",
    "output": output_file,
    "error": error_file,
}

app_info = {
    "application": "python",
    "input_file": "/dicos_ui_home/antonpr/ml/erdmann/airshower/PreProcessing_01.py",
    "working_dir": "/dicos_ui_home/antonpr/ml/erdmann/airshower",
}


run_job(slurm_directives, app_info, script_file)
