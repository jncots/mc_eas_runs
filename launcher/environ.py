from batch import output_env, run_job
from pathlib import Path


# root_res_dir = Path("/dicos_ui_home/antonpr/work/runs/ml/erdmann_02")
# script_file = root_res_dir / "script.sh"
# log_dir = root_res_dir / "logs"
# log_dirs = []
# for dname in ["output", "error"]:
#     d = log_dir / dname
#     d.mkdir(parents=True, exist_ok=True)
#     log_dirs.append(d)

# output_file = f"{log_dirs[0]}/%x-%A_%a.out"
# error_file = f"{log_dirs[1]}/%x-%A_%a.err"

output_file, error_file, script_file = output_env(
    "/dicos_ui_home/antonpr/work/runs/ml/erdmann_05"
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

# with open(script_file, "w") as f:
#     f.write(batch_script(slurm_directive, app))

# proc = subprocess.run(
#     ["sbatch", f"{script_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
# )

# print(proc.stdout.decode())
# err = proc.stderr.decode()
# if err.strip():
#     print(f"stderr:\n{err}")
