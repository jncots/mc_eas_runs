from pathlib import Path


def corsika_data_files(directory):
    base_path = Path("/dicos_ui_home/antonpr/work/corsika_runs")
    base_path = base_path / directory
    path_to_res = base_path/"results"

    corsika_datafiles = []
    for file in path_to_res.glob("DAT*[!.long]"):
        corsika_datafiles.append(file)
    
    return sorted(corsika_datafiles)


def print_missed_files(corsika_data_files_list):
    fnames = [int(f.name[-3:]) for f in corsika_data_files_list]

    iprev = 0
    ss = 0
    
    print_header = True
    for i in fnames[1:]:
        if i > iprev + 1:
            ss += (i - iprev - 1)
            if print_header:
                print(f"\n|Last before gap |First after gap |Number of missed |Total missed |")
                print(f"|-----------------------------------------------------------------|")
                print_header = False
            print(f"|{iprev:^16}|{i:^16}|{(i - iprev - 1):^17}|{ss:^13}|")
        iprev = i

    print(f"Total: found files = {len(fnames)}, missed = {ss}, missed + found =  {len(fnames) + ss}")
        
            
            
if __name__ == "__main__":
    data_files = corsika_data_files("34_simple_run")
    print_missed_files(data_files)
    
                