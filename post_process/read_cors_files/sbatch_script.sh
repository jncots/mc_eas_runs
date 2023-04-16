#!/bin/bash
#SBATCH --job-name=myjob
#SBATCH --nodes=50
#SBATCH --ntasks-per-node=12
#SBATCH --mem-per-cpu=4G
#SBATCH --time=0:01:00

#module load python/3.8.0

python parallel_script.py