from find_files import corsika_data_files
from pathlib import Path

def divide_to_batches(num_jobs, num_batches):
    batch_size = num_jobs//num_batches
    last_batch_id = num_batches - 1

    job_id_end = 0
    batches = []
    for batch_id in range(num_batches):
        job_id_start = job_id_end
        
        if batch_id != last_batch_id:
            job_id_end = job_id_start + batch_size  
        else:    
            job_id_end = num_jobs

        batches.append((batch_id, job_id_start, job_id_end))
    
    return batches

def create_sbatch(sbatch_params, run_number):
    
    corsika_runs_dir = "/dicos_ui_home/antonpr/work/corsika_runs"
    corsika_runs_dir = Path(corsika_runs_dir)
    
    current_run_dir = corsika_runs_dir/"spectrum_run"
    current_run_dir = current_run_dir/"04_sp_muon_run"
    current_run_dir = current_run_dir/"collect_data"
    current_run_dir.mkdir(parents=True, exist_ok=True)
    
    batch_file = current_run_dir/f"sbatch_run_{run_number}"
    with open("real_sbatch.sh") as ftemp:
        with open(batch_file, "w") as fout:
            fout.write(ftemp.read().format(**sbatch_params))

    return batch_file


if __name__ == '__main__':
    num_files = 10000
    num_batches = 17
    batches = divide_to_batches(num_files, num_batches)
    
    
    for batch in batches:
        batch_params = {        
        "job_name" : "my_job",
        "njobs" : 1,
        "cpus_per_task" : 10,
        "logs_dir" : "my_logs",
        "python_script" : "my_script.py",
        "batch_id" : batch[0],
        "start_job_id" : batch[1],
        "end_job_id" : batch[2],
        }
        
        
        create_sbatch(batch_params, batch[0])
        print(batch)   


