import sys
import json
import datetime
from itertools import groupby

'''
MIT License

Copyright (c) 2024 codeegenerates

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


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
    values = dict()
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
                    values[path] = 0
                else:
                    paths[path] = file_paths[idx-1]
                    values[path] = 0
            values[path]+=int(file.get('Effort')[:-2])
    for path, parent in paths.items():
        out_string += f" ['{path}', '{parent}', {values.get(path)}],"
    out_string += "]"
    return out_string


def process_second(json_str, html_template_path, reports_dir="."):
    # Parse the string into a json file
    json_data = json.loads(json_str)

    template_file_path = html_template_path
    try:
        with open(template_file_path, 'r') as template_file:
            template_content = template_file.read()
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
        template_content = template_content.replace(placeholder, str(value))

    # Write the modified HTML template to a new file
    filename = f"{reports_dir}/{json_data["git"]["Commit"]["Hash"]}__2.html"
    # Write the modified HTML template to a new file
    with open(filename, 'w') as f:
        f.write(template_content)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    # Read the JSON string from the command line
    json_str = sys.argv[1]
    html_template_path = sys.argv[2]

    # Open the json file
    with open(json_str, 'r') as file:
        json_str = file.read()

    process_second(json_str=json_str, html_template_path=html_template_path)