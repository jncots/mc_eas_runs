from pathlib import Path

base_dir = "/dicos_ui_home/antonpr/work/"
dir_with_runs = "corsika_runs"
corsika_inputs_template = "corsika_inputs_template"
corsika_sbatch_template = "corsika_sbatch_template"
corsika_launch_template = "launch_template"


python_script_dir = Path(__file__).parent
corsika_inputs_template = python_script_dir / corsika_inputs_template
corsika_sbatch_template = python_script_dir / corsika_sbatch_template
corsika_launch_template = python_script_dir / corsika_launch_template

template = {"inputs" : corsika_inputs_template,
            "sbatch" : corsika_sbatch_template,
            "launch" : corsika_launch_template}



def create_layout(run_name):
    base_dir = Path(base_dir)
    dir_with_runs = base_dir/dir_with_runs

    run_directory = dir_with_runs/run_name
    scripts_dir = run_directory/"scripts"
    logs_dir = run_directory/"logs"
    results_dir = run_directory/"results"

    run_layout = {"scripts_dir": scripts_dir, 
                  "logs_dir": logs_dir, 
                  "results_dir": results_dir}

    for directory in run_layout.values():
        directory.mkdir(parents=True, exist_ok=True)
        
    return run_layout


def create_inputs(run_layout, template, input_params, run_number):
    inputs_file = run_layout["scripts_dir"] / f"inputs_run_{run_number}"
    with open(template["inputs"]) as ftemp:
        with open(inputs_file, "w") as fout:
            fout.write(ftemp.read().format(**input_params))
    
    return inputs_file


def create_sbatch(run_layout, template, sbatch_params, run_number):
    batch_file = run_layout["scripts_dir"] / f"sbatch_run_{run_number}"
    with open(template["sbatch"]) as ftemp:   
        with open(batch_file, "w") as fout:
            fout.write(ftemp.read().format(**sbatch_params))