from pathlib import Path
import subprocess


def script_header(slurm_directive, shebang="#!/bin/bash", specifier="#SBATCH --"):
    header = shebang + "\n"
    for key, value in slurm_directive.items():
        if value is not None:
            header += f"\n{specifier}{key}={value}"
    header += "\n"
    return header


def script_body(app):
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
    output_dir = Path(output_path)
    script_file = output_dir / "script.sh"
    log_dir = output_dir / "logs"
    log_dirs = []
    for dname in ["output", "error"]:
        d = log_dir / dname
        d.mkdir(parents=True, exist_ok=True)
        log_dirs.append(d)

    output_file = f"{log_dirs[0]}/%x-%A_%a.out"
    error_file = f"{log_dirs[1]}/%x-%A_%a.err"
    return output_file, error_file, script_file


def run_job(slurm_directives, app_info, script_file):
    """Run sbatch job"""
    with open(script_file, "w") as f:
        f.write(batch_script(slurm_directives, app_info))

    proc = subprocess.run(
        ["sbatch", f"{script_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    print(proc.stdout.decode())
    err = proc.stderr.decode()
    if err.strip():
        print(f"stderr:\n{err}")
