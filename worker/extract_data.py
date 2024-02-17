#!/usr/bin/python3

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


import os
import sys
import subprocess
import json
import re
import smtplib
from email.mime.text import MIMEText
import traceback

EMAIL = "bananaeliteforces@gmail.com"
PASSWORD = "dtawogyinvochfsc"


def mail_warning(recipient, tag, commit):
    subject = f"Tag {tag} in commit {commit}"
    body = f"Tag {tag} in commit {commit}"
    try :
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL
        msg['To'] = recipient
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(EMAIL, PASSWORD)
            smtp_server.sendmail(EMAIL, recipient, msg.as_string())
    except:
        print("Error sending mail")
        traceback.print_exc()
        return
    
    
    
def tag_compile(input_text):
    pattern = re.compile(r"[A-Za-z][A-Za-z][A-Za-z]\d\d\d", re.IGNORECASE)
    return pattern.match(input_text)

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

config = False
only_tags = []
mail_list = []
if os.path.exists('codee_config.json') :
    config = True
    file = open('codee_config.json')
    config_param = json.load(file)
    if 'only-tags' in config_param.keys():
        for tag in config_param['only-tags']:
            is_valid = tag_compile(tag)
            if (is_valid):
                only_tags.append(tag)
    if 'mail-list' in config_param.keys():
        for pair in config_param['mail-list']:
            tags = []
            for tag in pair['tag']:
                tags.append(tag)
            mail_list.append((pair['mail'], tags))
            

# Get all files individually 
files_command = subprocess.run(["find", ".", "-type", "f"], capture_output=True, text=True)
files = files_command.stdout.split("\n")

# Run the screening phase to extract the data
# pwreport ./* --config build/compile_commands.json --screening --lang C --show-progress --exclude build/ --json
# pwreport --config build/compile_commands.json --screening --lang C --json --exclude build/


screening_command_line = [EXECUTABLE_NAME]
screening_command_line.extend(files)
if (len(only_tags) > 0):
    screening_command_line.append('--only-tags')
    screening_command_line.append(",".join(only_tags))
screening_command_line.extend(['--config', 'build/compile_commands.json', '--screening', '--lang', 'C', '--json','--accept-eula' ,'--exclude', 'build/'])
#print(screening_command_line)
screening_command_execution = subprocess.run(screening_command_line, capture_output=True, text=True)
try:
    screening_output = json.loads(screening_command_execution.stdout)
except:
    screening_output = ''
#with open(os.path.join(OUTPUT_DIR, "screening.json"), "w") as f:
#    json.dump(screening_output, f, indent=4)

# Run the checking phase to extract the data
checking_command_line = [EXECUTABLE_NAME]
checking_command_line.extend(files)
if (len(only_tags) > 0):
    checking_command_line.append('--only-tags')
    checking_command_line.append(",".join(only_tags))
checking_command_line.extend(['--config', 'build/compile_commands.json', '--checks', '--verbose', '--lang', 'C', '--json', '--accept-eula', '--exclude', 'build/'])
#print(checking_command_line)
checking_command_execution = subprocess.run(checking_command_line, capture_output=True, text=True)
checks = set()
try:
    checking_output = json.loads(checking_command_execution.stdout)
    
    for check_info in checking_output['Checks'] :
        if check_info['Check'] not in checks:
            checks.add(check_info['Check'])
except:
    checking_output = ''

#with open(os.path.join(OUTPUT_DIR, "checking.json"), "w") as f:
#    json.dump(checking_output, f, indent=4)

# Run git log
# git log --pretty=format:'{%n  "commit": "%H",%n  "abbreviated_commit": "%h",%n  "tree": "%T",%n  "abbreviated_tree": "%t",%n  "parent": "%P",%n  "abbreviated_parent": "%p",%n  "refs": "%D",%n  "encoding": "%e",%n  "subject": "%s",%n  "sanitized_subject_line": "%f",%n  "body": "%b",%n  "commit_notes": "%N",%n  "verification_flag": "%G?",%n  "signer": "%GS",%n  "signer_key": "%GK",%n  "author": {%n    "name": "%aN",%n    "email": "%aE",%n    "date": "%aD"%n  },%n  "commiter": {%n    "name": "%cN",%n    "email": "%cE",%n    "date": "%cD"%n  }}%n' -n 1

#git_command_line = ["git", "log", "--pretty=format:{%n  \"commit\": \"%H\",%n  \"abbreviated_commit\": \"%h\",%n  \"tree\": \"%T\",%n  \"abbreviated_tree\": \"%t\",%n  \"parent\": \"%P\",%n  \"abbreviated_parent\": \"%p\",%n  \"refs\": \"%D\",%n  \"encoding\": \"%e\",%n  \"subject\": \"%s\",%n  \"sanitized_subject_line\": \"%f\",%n  \"body\": \"%b\",%n  \"commit_notes\": \"%N\",%n  \"verification_flag\": \"%G?\",%n  \"signer\": \"%GS\",%n  \"signer_key\": \"%GK\",%n  \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }}%n", "-n", "1"]
git_command_line = ["/worker/get_git.sh"]
git_command_execution = subprocess.run(git_command_line, capture_output=True, text=True)
git_output = json.loads(git_command_execution.stdout)
commit = git_output['Commit']['Hash']

#### Send mail if necesary
if config:
    if len(mail_list) > 0:
        for mail_pair in mail_list:
            mail = mail_pair[0]
            tags = mail_pair[1]
            
            for tag in tags:
                if tag in checks:
                    mail_warning(mail, tag, commit)


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