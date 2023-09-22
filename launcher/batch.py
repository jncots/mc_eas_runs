from pathlib import Path

def script_header(job_options, 
                  shebang = "#!/bin/bash",
                  specifier = "# SBATCH --"):
    header = shebang + "\n"
    for key, value in job_options.items():
        if value is not None:
            header += f"\n{specifier}{key}={value}"
    header += "\n"
    return header  


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
    
