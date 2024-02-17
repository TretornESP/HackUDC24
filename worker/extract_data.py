#!/usr/bin/python3

import os
import sys
import subprocess
import json

# Read the parameters from the command line
if len(sys.argv) != 3:
    print("Usage: python3 extract_data.py <REPO_ROOT_PATH> <OUTPUT_DIR>")
    sys.exit(1)
REPO_ROOT_PATH = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

og_dir = os.getcwd()
EXECUTABLE_NAME = "pwreport"

# Create the output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Go to the root of the repository
os.chdir(REPO_ROOT_PATH)

# Take advantage of Codee integration with CMake 
# to generate a `compile_commands.json` file in the `build` directory.
# Execute the bash commands:
# cmake -DCMAKE_C_COMPILER=gcc -DCMAKE_EXPORT_COMPILE_COMMANDS=On -DCMAKE_BUILD_TYPE=Release -B build -G "Unix Makefiles" ./
# make -C build 
subprocess.run(['cmake', '-DCMAKE_C_COMPILER=gcc', '-DCMAKE_EXPORT_COMPILE_COMMANDS=On', '-DCMAKE_BUILD_TYPE=Release', '-B', 'build', '-G', 'Unix Makefiles', './'])
subprocess.run(['make', '-C', 'build'])

# Get all files individually 
files_command = subprocess.run(["find", ".", "-type", "f"], capture_output=True, text=True)
files = files_command.stdout.split("\n")

# Run the screening phase to extract the data
# pwreport ./* --config build/compile_commands.json --screening --lang C --show-progress --exclude build/ --json
# pwreport --config build/compile_commands.json --screening --lang C --json --exclude build/


screening_command_line = [EXECUTABLE_NAME]
screening_command_line.extend(files)
screening_command_line.extend(['--config', 'build/compile_commands.json', '--screening', '--lang', 'C', '--json', '--exclude', 'build/'])
screening_command_execution = subprocess.run(screening_command_line, capture_output=True, text=True)
screening_output = json.loads(screening_command_execution.stdout)

#with open(os.path.join(OUTPUT_DIR, "screening.json"), "w") as f:
#    json.dump(screening_output, f, indent=4)

# Run the checking phase to extract the data
checking_command_line = [EXECUTABLE_NAME]
checking_command_line.extend(files)
checking_command_line.extend(['--config', 'build/compile_commands.json', '--checks', '--verbose', '--lang', 'C', '--json', '--exclude', 'build/'])
checking_command_execution = subprocess.run(checking_command_line, capture_output=True, text=True)
checking_output = json.loads(checking_command_execution.stdout)

#with open(os.path.join(OUTPUT_DIR, "checking.json"), "w") as f:
#    json.dump(checking_output, f, indent=4)

# Run git log
# git log --pretty=format:'{%n  "commit": "%H",%n  "abbreviated_commit": "%h",%n  "tree": "%T",%n  "abbreviated_tree": "%t",%n  "parent": "%P",%n  "abbreviated_parent": "%p",%n  "refs": "%D",%n  "encoding": "%e",%n  "subject": "%s",%n  "sanitized_subject_line": "%f",%n  "body": "%b",%n  "commit_notes": "%N",%n  "verification_flag": "%G?",%n  "signer": "%GS",%n  "signer_key": "%GK",%n  "author": {%n    "name": "%aN",%n    "email": "%aE",%n    "date": "%aD"%n  },%n  "commiter": {%n    "name": "%cN",%n    "email": "%cE",%n    "date": "%cD"%n  }}%n' -n 1

#git_command_line = ["git", "log", "--pretty=format:{%n  \"commit\": \"%H\",%n  \"abbreviated_commit\": \"%h\",%n  \"tree\": \"%T\",%n  \"abbreviated_tree\": \"%t\",%n  \"parent\": \"%P\",%n  \"abbreviated_parent\": \"%p\",%n  \"refs\": \"%D\",%n  \"encoding\": \"%e\",%n  \"subject\": \"%s\",%n  \"sanitized_subject_line\": \"%f\",%n  \"body\": \"%b\",%n  \"commit_notes\": \"%N\",%n  \"verification_flag\": \"%G?\",%n  \"signer\": \"%GS\",%n  \"signer_key\": \"%GK\",%n  \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }}%n", "-n", "1"]
git_command_line = ["/worker/get_git.sh"]
git_command_execution = subprocess.run(git_command_line, capture_output=True, text=True)
git_output = json.loads(git_command_execution.stdout)

#with open(os.path.join(OUTPUT_DIR, "git.json"), "w") as f:
#    json.dump(git_output, f, indent=4)

# Write the output to a file
    
with open(os.path.join(OUTPUT_DIR, "full_output.json"), "w") as f:
    full_output = {
        "screening": screening_output,
        "checking": checking_output,
        "git": git_output
    }
    json.dump(full_output, f, indent=4)
    
os.chdir(og_dir)