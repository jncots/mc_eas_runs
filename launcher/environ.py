from batch import batch_script


output_dir = "out"
error_dir = "error"

job_options = {
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

app = {
    "application_dir" : "/dicos_ui_home/antonpr/work/",
    "application": "corsika75700Linux_SIBYLL_fluka",
    "input_file": "my_file",
    "working_dir": "/dicos_ui_home/antonpr/work/",
}

print(batch_script(job_options, app))