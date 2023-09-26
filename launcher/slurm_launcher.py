from pathlib import Path
import subprocess
import shutil


def script_header(slurm_directives, shebang="#!/bin/bash", specifier="#SBATCH --"):
    """
    Example of all options for slurm_directives:

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
    """

    header = shebang + "\n"
    for key, value in slurm_directives.items():
        if value is not None:
            header += f"\n{specifier}{key}={value}"
    header += "\n"
    return header


def script_body(app):
    """
    Example of all options for app:
    app = {
        "application_dir" : None,
        "application": "python",
        "options": {"-m" : "pip install",
                    "":"my_test.py"},
        "input_file": "my_file",
        "working_dir": "/dicos_ui_home/antonpr/work/",
    }
    """
    cwd = app["working_dir"]
    body = f"cd {cwd}"

    app_dir = app.get("application_dir", None)
    if app_dir is not None:
        app_exe = str(Path(app_dir) / app["application"])
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


def output_env(output_path):
    """Prepare directories for output

    Args:
        output_path (str, Path): root path for output

    Returns:
        output_file, error_file, script_file
    """
    root_dir = Path(output_path)
    output_dirs = []
    for dname in ["output", "error", "scripts"]:
        if dname == "scripts":
            d = root_dir / dname
        else:
            d = root_dir / "logs" / dname

        d.mkdir(parents=True, exist_ok=True)
        output_dirs.append(d)

    output_file = f"{output_dirs[0]}/%x-%A_%a.out"
    error_file = f"{output_dirs[1]}/%x-%A_%a.err"
    script_file = output_dirs[2] / "script.sh"
    return output_file, error_file, script_file


def backup_slurm_launcher(script_file):
    slurm_fw = Path(__file__)
    slurm_script = Path(__file__).parent / "slauncher_script.py"
    output_dir = script_file.parent
    for file in [slurm_fw, slurm_script]:
        shutil.copyfile(file, output_dir / file.name)


def run_job(slurm_directives, app_info, script_file):
    """Run sbatch job"""

    backup_slurm_launcher(script_file)
    with open(script_file, "w") as f:
        f.write(batch_script(slurm_directives, app_info))

    proc = subprocess.run(
        ["sbatch", f"{script_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    print(proc.stdout.decode())
    err = proc.stderr.decode()
    if err.strip():
        print(f"stderr:\n{err}")
