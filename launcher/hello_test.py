import os


job_info = {}
for env_var in ["SLURM_JOB_ID", "SLURM_ARRAY_JOB_ID", 
                "SLURM_ARRAY_TASK_ID", "SLURM_ARRAY_TASK_COUNT", 
                "SLURM_ARRAY_TASK_MAX", "SLURM_ARRAY_TASK_MIN"]:
    job_info[env_var] = os.environ.get(env_var)


for key, value in job_info.items():
    print(f"{key}={value}")