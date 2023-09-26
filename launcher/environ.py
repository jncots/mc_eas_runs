from batch import batch_script
import subprocess
from pathlib import Path


root_res_dir = Path("/dicos_ui_home/antonpr/work/runs/ml/erdmann_01")
log_dir = root_res_dir / "logs"
log_dirs = []
for dname in ["output", "error"]:
    d = log_dir / dname
    d.mkdir(parents=True, exist_ok=True)
    log_dirs.append(d)

output_file = f"{log_dirs[0]}/%x-%A_%a.out"
error_file = f"{log_dirs[1]}/%x-%A_%a.err"

slurm_directive = {
    "job-name": "test",
    "array": "0-99",
    "ntasks": 1,
    "mem": "3gb",
    "cpus-per-task": 10,
    "partition": "short_serial",
    "time": "01:00:00",
    "output": output_file,
    "error": error_file,
}

app = {
    "application": "python",
    "input_file": "/dicos_ui_home/antonpr/ml/erdmann/airshower/sim_par01.py",
    "working_dir": "/dicos_ui_home/antonpr/ml/erdmann/airshower",
}

# print(batch_script(job_options, app))
script_file = Path(__file__).parent / "script.sh"
with open(script_file, "w") as f:
    f.write(batch_script(slurm_directive, app))

proc = subprocess.run(
    ["sbatch", f"{script_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

print(proc.stdout.decode())
err = proc.stderr.decode()
if err.strip():
    print(f"stderr:\n{err}")
