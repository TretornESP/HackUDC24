#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import datetime

# Define a function to convert epoch time to UTC text-based date
def epoch_to_utc_text(epoch_time):
    utc_time = datetime.datetime.fromtimestamp(epoch_time, datetime.UTC)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S UTC')

def epoch_to_filename(epoch_time):
    utc_time = datetime.datetime.fromtimestamp(epoch_time, datetime.UTC)
    return utc_time.strftime('%Y_%m_%d_%H_%M_%S')

def argparse(sys_argv):
    # Check if the file path is provided as an argument
    if len(sys_argv) < 5:
        print(f"Usage: python3 {sys_argv[0]} <screening.json> <checking.json> <commit.json> <template.html>")
        sys.exit(1)

    # Get the file path from the command line argument
    screening_json_file_path = sys_argv[1]
    try:
        # Open the JSON file
        with open(screening_json_file_path) as f:
            screening_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{screening_json_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{screening_json_file_path}' is not a valid JSON file.")
        sys.exit(1)

    # Get the file path from the command line argument
    checking_json_file_path = sys_argv[2]
    try:
        # Open the JSON file
        with open(checking_json_file_path) as f:
            checking_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{checking_json_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{checking_json_file_path}' is not a valid JSON file.")
        sys.exit(1)


    # Get the file path from the command line argument
    commit_json_file_path = sys_argv[3]
    try:
        # Open the JSON file
        with open(commit_json_file_path) as f:
            commit_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{commit_json_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{commit_json_file_path}' is not a valid JSON file.")
        sys.exit(1)
    
    template_file_path = sys_argv[4]
    try:
        with open(template_file_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_file_path}' not found.")
        sys.exit(1)
    
    return (screening_data, checking_data, commit_data, template_content)

def populate_lX_checks(checks_list_lX, color):
    # Replace placeholders in the red box wrapper
    color_box_content = []
    for check in checks_list_lX:
        # Check if subtitle and code are not None
        if check["Auto-fix"]:
            mouseover_description = f'<div class="suggestion-icon">!<span class="suggestion-icon-text"><div class="text-wrapper">{'<br>'.join(check["Auto-fix"])}</div></span></div>'
        else:
            mouseover_description = ''
        
        color_box_content.append(f'''
        <div class="checkbox {color}">
            <div>
                <a href="{check['Documentation']}">{check['Check']}</a>: {check['Title']}
                {mouseover_description}
            </div>
            <hr>
            <div>
                <p>Location: {check['Location']}</p>
                <p>Suggestion: {check['Suggestion']}</p>
                {f'<p>Related code: {check["Subtitle"]}</p>' if check["Subtitle"] else ''}
                {f'<textarea readonly rows="3" class="related_code {color}">\n{'\n'.join(check['Code'])}</textarea>' if check["Code"] else ''}
            </div>
        </div>
        ''')
    return '\n'.join(color_box_content)

def main():
    (screening_data, checking_data, commit_data, html_template) = argparse(sys.argv)

    # Extract Analysis data
    checking_analysis = checking_data['Analysis']
    checking_elapsed_ms = checking_analysis['ElapsedMillis']
    checking_compiler_flags = checking_analysis['CompilerFlags']
    if checking_compiler_flags == '':
        checking_compiler_flags = '-'

    # Initialize lists for different levels of checks
    checks_list_l1 = []
    checks_list_l2 = []
    checks_list_l3 = []

    # Extract checks data
    checks = checking_data['Checks']
    for check in checks:
        # Extract common fields
        check_data = {
            "Check": check["Check"],
            "Location": check["Location"],
            "Title": check["Title"],
            "Suggestion": check["Suggestion"],
            "Auto-fix": check["Auto-fix"],
            "Documentation": check["Documentation"],
            "Subtitle": check["RelatedCodeList"]["Subtitle"] if check["RelatedCodeList"] else None,
            "Code": check["RelatedCodeList"]["Code"] if check["RelatedCodeList"] else None
        }
        # Extract additional fields based on level
        level = check["Level"]
        if level == "L1":
            checks_list_l1.append(check_data)
        elif level == "L2":
            checks_list_l2.append(check_data)
        elif level == "L3":
            checks_list_l3.append(check_data)

    # Parse commit data
    git_repository_name = commit_data["Repository"]["Name"]
    git_repository_url = commit_data["Repository"]["URL"]
    git_branch = commit_data["Branch"]
    git_commit_hash = commit_data["Commit"]["Hash"]
    git_commit_url = commit_data["Commit"]["URL"]
    git_author = commit_data["Author"]
    git_date_epoch = int(commit_data["Date"])
    git_message = commit_data["Message"]

    # Print or do whatever you want with the extracted data
    print("Elapsed Millis:", checking_elapsed_ms)
    print("Compiler Flags:", checking_compiler_flags)
    print("\nChecks Level 1:")
    for check in checks_list_l1:
        print(check)
    print("\nChecks Level 2:")
    for check in checks_list_l2:
        print(check)
    print("\nChecks Level 3:")
    for check in checks_list_l3:
        print(check)

    print("\nGit Repository Name:", git_repository_name)
    print("Git Repository URL:", git_repository_url)
    print("Git Branch:", git_branch)
    print("Git Commit Hash:", git_commit_hash)
    print("Git Commit URL:", git_commit_url)
    print("Git Author:", git_author)
    print("Git Date (Epoch):", git_date_epoch)
    print("Git Date (UTC):", epoch_to_utc_text(git_date_epoch))
    print("Git Message:", git_message)



    # Replace placeholders in the HTML template with the extracted data
    placeholders = {
        "$commit$": git_commit_hash,
        "$repository_url$": git_repository_url,
        "$repository$": git_repository_name,
        "$branch$": git_branch,
        "$commit_url$": git_commit_url,
        "$author$": git_author,
        "$date$": epoch_to_utc_text(git_date_epoch),
        "$message$": git_message,

        "$elapsed$": checking_elapsed_ms,
        "$flags$": checking_compiler_flags,

        "$checkboxes_red$":    populate_lX_checks(checks_list_l1, "red"),
        "$checkboxes_yellow$": populate_lX_checks(checks_list_l2, "yellow"),
        "$checkboxes_green$":  populate_lX_checks(checks_list_l3, "green"),
    }
    
    for placeholder, value in placeholders.items():
        html_template = html_template.replace(placeholder, str(value))
    
    # Write the modified HTML template to a new file
    with open(f"{epoch_to_filename(git_date_epoch)}.html", 'w') as f:
        f.write(html_template)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()