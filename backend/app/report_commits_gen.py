import sys
import json
import datetime
from itertools import groupby

def parse_path(path):
    """
    Parse the path and return the filename and the path.
    """
    path = path[2:] if path.startswith("./") else path
    filename = path.split("/")[-1]
    # I want all the intermediate files
    # Ej. for path = "a/b/c/d/file.txt" I want "a", "a/b", "a/b/c" and "a/b/c/d"
    folders = path.split("/")[:-1]
    file_paths = ["/".join(folders[:i+1]) for i in range(len(folders))]
    return file_paths, path

def parse_treeview_rows(full_json):
    """
    Parse the treeview widget and return a list of the items in the treeview.
    """
    checks = full_json["checking"]["Checks"]
    fix, nofix = [], []
    for x in checks:
      (fix, nofix)[x.get("Auto-fix") == [] ].append(x)

    new_fix = [j.get("Check") for j in fix]
    new_nofix = [j.get("Check") for j in nofix]

    fix_grouped = {k: len(list(v)) for k, v in groupby(new_fix)}
    nofix_grouped = {k: len(list(v)) for k, v in groupby(new_nofix)}

    out_string = "[['Fixable-Issues', null, 0]"
    out_string += ", ['Auto-fixable', 'Fixable-Issues', 0]"
    out_string += ", ['Non Auto-fixable', 'Fixable-Issues', 0]"
    for k, v in fix_grouped.items():
        out_string += f", ['{k}', 'Auto-fixable', {v}]"
    for k, v in nofix_grouped.items():
        out_string += f", ['{k}', 'Non Auto-fixable', {v}]"
    out_string += "]"

    return out_string

def parse_files_rows(full_json):
    """
    Parse the files widget and return a list of the items in the files widget.
    """
    files = full_json["screening"]["Evaluation"][0]
    out_string = "[['Paths', null, 0],"
    paths = dict()
    main_path = "Paths"
    for file in files:
        if file.get("Target") == "Total":
            continue
        file_paths, filename = parse_path(file.get("Target"))
        out_string += f" ['{filename}', '{file_paths[-1] if len(file_paths) else main_path}', {file.get('Effort')[:-2]}],"
        for idx, path in enumerate(file_paths):
            if path not in paths:
                if idx == 0:
                    paths[path] = "Paths"
                else:
                    paths[path] = file_paths[idx-1]
    for path, parent in paths.items():
        out_string += f" ['{path}', '{parent}', 0],"
    out_string += "]"
    return out_string


def main():
    
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <data.json> <template.html>")
        sys.exit(1)

    # Get the file path from the command line argument
    json_file_path = sys.argv[1]
    try:
        # Open the JSON file
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{json_file_path}' is not a valid JSON file.")
        sys.exit(1)

    template_file_path = sys.argv[2]
    try:
        with open(template_file_path, 'r') as template_file:
            html_template = template_file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_file_path}' not found.")
        sys.exit(1)

    #### Generate tree view rows
    treeview_rows = parse_treeview_rows(json_data)
    file_rows = parse_files_rows(json_data)

    placeholders = {
        "$treeview_rows$": treeview_rows,
        "$files_rows$": file_rows,
    }

    for placeholder, value in placeholders.items():
        html_template = html_template.replace(placeholder, str(value))

    # Write the modified HTML template to a new file
    with open(f"last_temp_report.html", 'w') as f:
        f.write(html_template)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()