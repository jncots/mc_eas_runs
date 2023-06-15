import subprocess
from pathlib import Path
from tqdm import tqdm

python_script_dir = Path(__file__).parent

launch_file = "sbatch_script.sh"
launch_file = python_script_dir/launch_file

proc = subprocess.Popen([f"{launch_file}"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)

while proc.poll() is None:
    print(proc.stderr.readline())
print(proc.stdout.read())
proc.stdout.close()

# while True:
#     line = proc.stderr.readline()
#     if not line:
#         break
#     print(line.decode())
# for line in proc.stderr:
#         # # Update tqdm progress bar based on the output
#         # # Assuming the output contains progress information (e.g., percentage)
#         # progress = parse_progress_from_output(line)  # Implement this function according to your specific output format
#         # tqdm.update(line)
#         print(line.decode())

    # Wait for the subprocess to finish
proc.wait()

# print(f"stdout:\n{proc.stdout.decode()}")
# print(f"stderr:\n{proc.stderr.decode()}")

# def launch_slurm_script():
#     slurm_process = subprocess.Popen(['sbatch', 'your_slurm_script.sh'], 
#                                      stdout=subprocess.PIPE, 
#                                      stderr=subprocess.PIPE, 
#                                      universal_newlines=True)

#     # Read the subprocess output line by line
#     for line in slurm_process.stdout:
#         # Update tqdm progress bar based on the output
#         # Assuming the output contains progress information (e.g., percentage)
#         progress = parse_progress_from_output(line)  # Implement this function according to your specific output format
#         tqdm.update(progress)

#     # Wait for the subprocess to finish
#     slurm_process.wait()