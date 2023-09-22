# SBATCH --job-name=corsika_run5
# SBATCH --array=1-1
# SBATCH --ntasks=1                    # Run on a single CPU
# SBATCH --mem=3gb                     # Job memory request
# SBATCH --cpus-per-task=1
# SBATCH --partition=short_serial
# SBATCH --time=01:00:00               # Time limit hrs:min:sec
# SBATCH --output=/dicos_ui_home/antonpr/work/corsika_runs/14_simple_run/logs/%x.%J.out
# SBATCH --error=/dicos_ui_home/antonpr/work/corsika_runs/

from pathlib import Path
output_dir = "out"
error_dir = "error"

default_options = {
    "job-name": "test",
    "array": "1-1",
    "ntasks": 1,
    "mem": "3gb",
    "cpus-per-task": 1,
    "partition": "short_serial",
    "time": "01:00:00",
    "output": output_dir,
    "error": error_dir,
}

def script_header(job_options, 
                  shebang = "#!/bin/bash",
                  specifier = "# SBATCH --"):
    header = shebang + "\n"
    for key, value in job_options.items():
        if value is not None:
            header += f"\n{specifier}{key}={value}"
    header += "\n"
    return header  

# print(script_header(default_options))

# # Corsika paths
# root_dir=/dicos_ui_home/antonpr/work/
# corsika_dir=${root_dir}/cors_fluka/corsika-75700/run/
# corsika_exe=corsika75700Linux_SIBYLL_fluka

# # Run
# cd ${corsika_dir}
# ./${corsika_exe} < /dicos_ui_home/antonpr/work/corsika_runs/14_simple_run/scripts/inputs_run_5

# app = {
#     "application_dir" : None,
#     "application": "python",
#     "options": {"-m" : "pip install",
#                 "":"my_test.py"},
#     "input_file": "my_file",
#     "working_dir": "/dicos_ui_home/antonpr/work/",
# }


app = {
    "application_dir" : "/dicos_ui_home/antonpr/work/",
    "application": "corsika75700Linux_SIBYLL_fluka",
    "input_file": "my_file",
    "working_dir": "/dicos_ui_home/antonpr/work/",
}

# Run
# cd ${corsika_dir}
# ./${corsika_exe} < /dicos_ui_home/antonpr/wo

def script_body(app):
    cwd = app["working_dir"]
    body = f"cd {cwd}"
    
    app_dir = app.get("application_dir", None)
    if app_dir is not None:
        app_exe = str(Path(app_dir)/app["application"])
    else:
        app_exe = app["application"]
    body += f"\n{app_exe} "
    
    options = app.get("options", None)
    if options is not None:
        for key, value in options.items():
            body += f"{key} {value} "
    
    input_file = app.get("input_file", None)
    if input_file is not None:
        body += f"< {input_file}"
        
    return body    


def batch_script(job_options, app):
    script = script_header(job_options) + "\n"
    script += script_body(app)
    return script
    
    
print(batch_script(default_options, app))
    
