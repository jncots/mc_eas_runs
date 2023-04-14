from pathlib import Path
import os

base_path = Path("/dicos_ui_home/antonpr/work/corsika_runs")
base_path = base_path / "21_simple_run"
path_to_res = base_path/"logs"

corsika_datafiles = []
for file in path_to_res.glob("*.err"):
    corsika_datafiles.append(file)

corsika_datafiles = sorted(corsika_datafiles) 

for file in corsika_datafiles:
    if not os.stat(file).st_size == 0:
        print(str(file))
    with open(file) as f:
        content = f.read()
        for line in content.split("\n"):
            if line.strip():
                print(line)