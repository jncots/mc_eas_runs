from pathlib import Path
import json

def add_to_templ(templ):
    
    new_dict = {}
    new_dict["option"] = "OBSLEV"
    new_dict["values"] = ["{df}", "{pdf}", "{test}"]
    new_dict["description"] = "Some description"
    
    templ.append(new_dict)


base_num = 0
new_num = 1
base_dir = Path(__file__).parent
base_json = base_dir/f"base_template_{base_num}.json"
new_json = base_dir/f"base_template_{new_num}.json"
new_inputs = base_dir/f"inputs.inp"

with open(base_json) as file:
    templ_json = json.load(file)

add_to_templ(templ_json)
with open(new_json, "w") as file:
    json.dump(templ_json, file, sort_keys=True, indent=4)


inputs_str = ""
for option in templ_json:
    opt_name = option["option"]
    opt_values = ""
    for opt_val in option["values"]:
        opt_values += f"{opt_val} "
        
    opt_desc = option["description"]
    inputs_str += f"{opt_name} {opt_values} {opt_desc}"
    
with open(new_inputs, "w") as file:
    file.write(inputs_str) 