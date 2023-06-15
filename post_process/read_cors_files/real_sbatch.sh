#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --array=1-{njobs}
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --mem=3gb                     # Job memory request
#SBATCH --cpus-per-task={cpus_per_task}
#SBATCH --partition=short_serial
#SBATCH --time=00:10:00               # Time limit hrs:min:sec
#SBATCH --output={logs_dir}/%x.%J.out
#SBATCH --error={logs_dir}/%x.%J.err


srun python {python_script} {batch_id} {start_job_id} {end_job_id}
